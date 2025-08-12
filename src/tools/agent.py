from openai import OpenAI
from pathlib import Path
import sys

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.tools.db_tools import HeartDiseaseDBTool, CancerDBTool, DiabetesDBTool
from src.tools.web_search import MedicalWebSearchTool
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class MedicalAgent:
    def __init__(self):
        """Initialize the medical agent with OpenAI client and tools"""
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("BASE_URL")
        )
        self.heart_tool = HeartDiseaseDBTool()
        self.cancer_tool = CancerDBTool()
        self.diabetes_tool = DiabetesDBTool()
        self.web_tool = MedicalWebSearchTool()

    def _is_data_query(self, query: str) -> bool:
        """
        Determine if the query is about data/statistics or general medical knowledge.
        """
        data_keywords = [
            "average", "mean", "median", "statistics", "data", "distribution",
            "count", "number", "percentage", "ratio", "compare", "analysis",
            "how many", "what percentage", "correlation", "trend"
        ]
        return any(keyword in query.lower() for keyword in data_keywords)

    def _format_df_response(self, df: pd.DataFrame, query: str) -> str:
        """
        Format DataFrame results into natural language response using GPT.
        """
        df_info = df.to_string()
        messages = [
            {"role": "system", "content": "You are a medical data analyst. Format the data results into a clear, natural language response."},
            {"role": "user", "content": f"Query: {query}\nData Results:\n{df_info}"}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content

    def process_query(self, query: str) -> str:
        """
        Process user query and route to appropriate tool.
        """
        try:
            if self._is_data_query(query):
                # Determine which database to use
                if any(word in query.lower() for word in ["heart", "cardiac", "cardiovascular"]):
                    df = self.heart_tool.execute_query(self._generate_sql_query(query, "heart_disease"))
                    return self._format_df_response(df, query)
                
                elif any(word in query.lower() for word in ["cancer", "tumor", "malignant"]):
                    df = self.cancer_tool.execute_query(self._generate_sql_query(query, "cancer"))
                    return self._format_df_response(df, query)
                
                elif any(word in query.lower() for word in ["diabetes", "glucose", "insulin"]):
                    df = self.diabetes_tool.execute_query(self._generate_sql_query(query, "diabetes"))
                    return self._format_df_response(df, query)
                
                else:
                    return "Please specify which medical condition (heart disease, cancer, or diabetes) you're asking about."
            
            else:
                # Use web search for general medical knowledge
                search_results = self.web_tool.search(query)
                
                messages = [
                    {"role": "system", "content": "You are a medical knowledge assistant. Provide accurate, helpful information based on search results."},
                    {"role": "user", "content": f"Based on these search results, answer the query: {query}\nResults: {search_results}"}
                ]
                
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.7
                )
                return response.choices[0].message.content
                
        except Exception as e:
            return f"Error processing query: {str(e)}"

    def _generate_sql_query(self, user_query: str, table_name: str) -> str:
        """
        Generate SQL query from natural language using GPT.
        """
        messages = [
            {"role": "system", "content": f"You are a SQL query generator. Generate a SQL query for the {table_name} table based on the user's question."},
            {"role": "user", "content": user_query}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.1
        )
        return response.choices[0].message.content
