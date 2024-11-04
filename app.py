import os
from typing import Optional
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from db_parse import db_parser
from csv_parse import csv_parser


def initialize_session_state():
    """Initialize session state variables."""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_file' not in st.session_state:
        st.session_state.current_file = None
    if 'df_preview' not in st.session_state:
        st.session_state.df_preview = None


def display_chat_history():
    """Display the chat history in a conversational format."""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def add_message(role: str, content: str):
    """Add a message to the chat history."""
    st.session_state.chat_history.append({"role": role, "content": content})


def load_csv_file(user_file) -> Optional[pd.DataFrame]:
    """Load and validate CSV file."""
    try:
        df = pd.read_csv(user_file)
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")
        return None


def display_file_info(df: pd.DataFrame):
    """Display basic information about the loaded dataset."""
    with st.expander("Dataset Information", expanded=False):
        st.write(f"Number of rows: {len(df)}")
        st.write(f"Number of columns: {len(df.columns)}")
        st.write("Columns:", ", ".join(df.columns))
        st.write("Preview of the data:")
        st.dataframe(df.head(), use_container_width=True)


def main():
    # Load environment variables
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    if not GEMINI_API_KEY:
        st.error("API key not found. Please set your GEMINI_API_KEY in the .env file.")
        return

    # Initialize session state
    initialize_session_state()

    # Set Streamlit page configuration
    st.set_page_config(
        page_title="Chat with Your Data",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Main header with custom styling
    st.markdown("""
        <h1 style='text-align: center;'>Chat with Your Data 📊</h1>
        <p style='text-align: center;'>Upload your dataset and ask questions in natural language</p>
    """, unsafe_allow_html=True)

    # Sidebar configuration
    with st.sidebar:
        st.markdown("## Configuration ⚙️")
        file_type = st.selectbox(
            "Select your data source:",
            options=["CSV", "MySQL database"],
            help="Choose the type of data you want to analyze"
        )

        # Add a divider
        st.divider()

        # Display usage tips
        st.markdown("### 📝 Usage Tips")
        st.markdown("""
        - Upload your data file or connect to database
        - Ask questions in plain English
        - View the data preview before asking questions
        - Check the chat history for previous interactions
        """)

    # Main content area
    if file_type == "CSV":
        col1, col2 = st.columns([2, 1])

        with col1:
            user_file = st.file_uploader(
                "Upload your CSV dataset:",
                type="csv",
                help="Upload a CSV file to analyze"
            )

            if user_file:
                if user_file != st.session_state.current_file:
                    with st.spinner("Loading dataset..."):
                        df = load_csv_file(user_file)
                        if df is not None:
                            st.session_state.current_file = user_file
                            st.session_state.df_preview = df
                            st.success("File loaded successfully!")

                if st.session_state.df_preview is not None:
                    display_file_info(st.session_state.df_preview)

        with col2:
            st.markdown("### Ask Questions 💭")
            user_input = st.text_area(
                "Enter your question:",
                placeholder="e.g., 'What is the average age of passengers?'",
                help="Ask questions about your data in plain English"
            )

            if st.button("Ask Question", type="primary"):
                if not user_input:
                    st.warning("Please enter a question.")
                else:
                    with st.spinner("Analyzing..."):
                        add_message("user", user_input)
                        try:
                            response = csv_parser(
                                user_file=user_file,
                                user_input=user_input,
                                api_key=GEMINI_API_KEY
                            )
                            if response:
                                add_message("assistant", response)
                            else:
                                add_message("assistant",
                                            "I couldn't analyze the data. Please try rephrasing your question.")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")

    elif file_type == "MySQL database":
        st.markdown("### Database Connection 🔌")

        # Database connection form
        with st.form("database_connection"):
            db_host = st.text_input("Host:", placeholder="localhost")
            db_user = st.text_input("Username:")
            db_password = st.text_input("Password:", type="password")
            db_name = st.text_input("Database name:")


            submit_button = st.form_submit_button("Connect")

            if submit_button:
                if all([db_host, db_user, db_password, db_name]):
                    with st.spinner("Connecting to database..."):
                        try:
                            response = db_parser(db_host=db_host, db_user=db_user, db_password=db_password,
                                                 db_name=db_name)

                            st.success("Connected successfully!")
                            st.write(response)
                        except Exception as e:
                            st.error(f"Connection failed: {str(e)}")
                else:
                    st.warning("Please fill in all database connection fields.")

    # Display chat history
    st.markdown("### Chat History 💬")
    display_chat_history()


if __name__ == "__main__":
    main()