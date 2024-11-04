from langchain_experimental.agents import create_csv_agent
from langchain_google_genai import ChatGoogleGenerativeAI


def format_response(response):
    """Formats the response from the agent into a natural language output."""
    if response is None:
        return "Unfortunately, I didn't receive any response from the agent."

    output = response.get("output")
    if output is None:
        return "It seems the agent did not return a valid output."

    # Construct a natural language response
    natural_language_response = "### Analysis Result\n\n"

    # Convert the output into a natural language format
    if isinstance(output, dict):
        for key, value in output.items():
            natural_language_response += f"The {key} is {value}.\n"
    elif isinstance(output, list):
        natural_language_response += "Here are some insights:\n"
        for item in output:
            natural_language_response += f"- {item}.\n"
    else:
        natural_language_response += f"Based on the data, I found the following result: {output}.\n"

    # Final conclusion
    natural_language_response += "\n---\n*This analysis is based on the provided data. Feel free to ask more questions for deeper insights!*"

    return natural_language_response


def csv_parser(user_file, user_input, api_key):
    """Handles CSV operations: asks questions to the dataset."""
    if user_file and user_input:
        # Initialize the Gemini model
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)

        try:
            # Create the CSV agent
            agent_executor = create_csv_agent(llm, user_file, verbose=True, allow_dangerous_code=True)
            # Run the agent with the user's question
            response = agent_executor.invoke(user_input)
            print(f"CSV parser response: {response}")  # Debug print statement

            # Format the response before returning
            return format_response(response)
        except Exception as e:
            print(f"Error in csv_parser: {e}")  # Debug print statement
            return "An error occurred while processing your request."

    return "Please provide both a CSV file and a question."
