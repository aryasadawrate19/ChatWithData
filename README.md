# Data Chat Assistant 📊

A Streamlit-based web application that allows users to interact with their data through natural language queries. The application supports both CSV files and MySQL databases, powered by Google's Gemini API for natural language processing.

## Features 🌟

- **CSV File Analysis**
  - Upload and analyze CSV datasets
  - Interactive data preview
  - Natural language queries
  - Real-time data visualization
  - Chat history tracking

- **MySQL Database Integration**
  - Secure database connection
  - Query databases using natural language
  - Database schema visualization
  - Connection state management

- **User Interface**
  - Clean, intuitive design
  - Responsive layout
  - Progress indicators
  - Error handling and user feedback
  - Detailed dataset information

## Prerequisites 📋

Before running the application, make sure you have Python 3.8+ installed on your system. You'll also need:

- A Google Cloud account with Gemini API access
- Python virtual environment (recommended)
- MySQL server (if using database features)

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/yourusername/data-chat-assistant.git
cd data-chat-assistant
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage 💡

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. For CSV analysis:
   - Select "CSV" as your data source
   - Upload your CSV file
   - View the data preview
   - Ask questions about your data in natural language

4. For MySQL database analysis:
   - Select "MySQL database" as your data source
   - Enter your database credentials
   - Connect to your database
   - Start querying your data using natural language

## Example Queries 📝

Here are some example questions you can ask about your data:

- "What is the average age of passengers?"
- "Show me the top 5 countries by revenue"
- "Create a histogram of sales distribution"
- "Find correlations between age and income"
- "What was the total revenue for each quarter?"

## Project Structure 📁

```
data-chat-assistant/
├── app.py              # Main Streamlit application
├── csv_parse.py        # CSV processing module
├── db_parse.py         # Database processing module
├── requirements.txt    # Project dependencies
├── .env               # Environment variables
└── README.md          # Project documentation
```

## Configuration ⚙️

The application can be configured through the following environment variables:

- `GEMINI_API_KEY`: Your Google Gemini API key


## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security Considerations 🔒

- Never commit your `.env` file or expose your API keys
- Use secure database connections
- Implement proper input validation
- Follow security best practices when deploying

## Troubleshooting 🔍

Common issues and solutions:

1. **API Key Issues**
   - Ensure your API key is correctly set in the `.env` file
   - Verify API key permissions in Google Cloud Console

2. **Database Connection Issues**
   - Check database credentials
   - Verify database server is running
   - Ensure proper network connectivity

3. **CSV Upload Issues**
   - Verify CSV file format
   - Check file encoding (UTF-8 recommended)
   - Ensure file size is within limits



## Acknowledgments 🙏

- Google Gemini API for natural language processing
- Streamlit team for the amazing framework
- All contributors and users of this project

