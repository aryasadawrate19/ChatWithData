import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def init_db(db_user: str, db_password: str, db_host: str, db_port: str, db_name: str) -> SQLDatabase:
    db_uri = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return SQLDatabase.from_uri(db_uri)


def get_sqlchain(db):
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    Question: Which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) as track_count from Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
    
    Question: Name 10 artists
    SQL Query: SELECT Name FROM Artist LIMIT 10;
    
    Your turn:
    Question: {question}
    SQL Query:
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    def get_schema(_):
        return db.get_table_info()

    return (
            RunnablePassthrough.assign(schema=get_schema)
            | prompt
            | llm
            | StrOutputParser()
    )


def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    sql_chain = get_sqlchain(db)

    template = """
    You are a data analyst at a company. You are interacting with a user who is asking questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User Question: {question}
    SQL Response: {response}
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda var: db.run(var["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({
        "question": user_query,
        "chat_history": chat_history
    })


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage("Hello! I am a SQL Assistant. Ask me anything about your database."),
        HumanMessage(content="How many albums are there in the database?"),
    ]

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Chat with MySQL", page_icon=":speech_balloon:")

st.title("Chat With Data")

with st.sidebar:
    st.subheader("Settings")
    st.write("Connect to the db")

    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Port", value="3306", key="Port")
    st.text_input("User", value="root", key="User")
    st.text_input("Password", type="password", key="Password")
    st.text_input("Name of the Database", key="Database")

    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            db = init_db(
                db_user=st.session_state["User"],
                db_password=st.session_state["Password"],
                db_host=st.session_state["Host"],
                db_port=st.session_state["Port"],
                db_name=st.session_state["Database"]
            )
            st.session_state.db = db

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
user_query = st.chat_input("Type a message")

if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        sql_chain = get_sqlchain(st.session_state.db)
        response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
        # response = "I don't know how to respond to that."
        st.markdown(response)

        st.session_state.chat_history.append(AIMessage(content=response))
