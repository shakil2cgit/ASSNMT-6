# Medical AI Agent

A Multi-Tool AI Agent that can interact with medical datasets and provide general medical knowledge.

## Features

- Query and analyze three medical datasets:
  - Heart Disease Dataset
  - Cancer Dataset
  - Diabetes Dataset
- Get general medical information using web search
- Natural language interface via Streamlit
- SQL database integration
- OpenAI GPT-powered responses

## Setup Instructions

1. **Install SQLite** (if not already installed):

   For Windows:
   ```bash
   winget install --id=SQLite.sqlite --source=winget
   ```

   For Linux:
   ```bash
   sudo apt install sqlite3
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/Mac
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   - Copy `.env.template` to a new file named `.env`
   - Fill in your API keys in the `.env` file
   ```
   OPENAI_API_KEY=your_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   BASE_URL=https://api.artemox.com/v1
   ```
   Note: Never commit your actual API keys to version control!

5. **Initialize Databases**:
   ```bash
   python src/utils/setup_db.py
   ```

6. **Run the Application**:
   ```bash
   streamlit run src/main.py
   ```

## Project Structure

```
medical-ai-agent/
├── data/
│   ├── db/              # SQLite databases
│   └── raw/             # Original CSV files
├── src/
│   ├── tools/           # Database and web search tools
│   ├── utils/           # Utility functions
│   └── main.py          # Main Streamlit application
├── .env                 # Environment variables
└── requirements.txt     # Python dependencies
```

## Usage Examples

1. **Data Analysis Queries**:
   - "What is the average age of heart disease patients?"
   - "Show me the distribution of cancer types"
   - "What's the correlation between age and diabetes?"

2. **Medical Knowledge Queries**:
   - "What are the symptoms of heart disease?"
   - "How is cancer diagnosed?"
   - "What are the risk factors for diabetes?"

## Technologies Used

- OpenAI GPT for natural language processing
- Streamlit for web interface
- SQLite for database management
- Tavily API for web search
- Pandas for data manipulation
- SQLAlchemy for database operations

## Notes

- The system automatically determines whether to use the database tools or web search based on the query type
- Data queries use SQL databases for fast and accurate results
- General medical queries use web search to provide up-to-date information

## License

MIT License
