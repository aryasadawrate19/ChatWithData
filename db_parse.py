import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialize language model
llm = ChatGoogleGenerativeAI(model="gemini-pro",)

# Database connection function
def db_parser(db_host, db_user, db_password, db_name):
    db_uri = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
    global db
    db = SQLDatabase.from_uri(db_uri)

# Function to retrieve schema
def get_schema():
    return db.get_table_info()

# SQL generation chain template
sql_template = """
Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:
"""
sql_prompt = ChatPromptTemplate.from_template(sql_template)

# SQL query generation chain
sql_chain = (
    RunnablePassthrough.assign(schema=lambda: get_schema())
    | sql_prompt
    | llm.bind(stop="\nSQL Result:")
    | StrOutputParser()
)

# Natural language response generation template
response_template = """
Based on the table schema below, question, sql query, and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}
"""
response_prompt = ChatPromptTemplate.from_template(response_template)

# Full conversational chain for response
full_chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
        schema=lambda: get_schema(),
        response=lambda vars: run_query(vars["query"])
    )
    | response_prompt
    | llm
    | StrOutputParser()
)

# Function to execute SQL query
def run_query(query):
    return db.run(query)

# Function to run the full conversational chain and get the response
def generate_response(question):
    response = full_chain.invoke({
        "question": question,
        "schema": get_schema()
    })
    return response
