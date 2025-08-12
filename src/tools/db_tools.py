from pathlib import Path
import sqlite3
from typing import List, Dict, Any
import pandas as pd

class BaseDBTool:
    def __init__(self, db_name: str):
        """
        Initialize database tool with database name.
        
        Args:
            db_name (str): Name of the database file (e.g., 'heart_disease.db')
        """
        self.db_path = Path(__file__).parent.parent.parent / "data" / "db" / db_name
        
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute SQL query and return results as a pandas DataFrame.
        
        Args:
            query (str): SQL query to execute
            
        Returns:
            pd.DataFrame: Query results
        """
        conn = sqlite3.connect(self.db_path)
        try:
            df = pd.read_sql_query(query, conn)
            return df
        finally:
            conn.close()
            
    def get_schema(self) -> str:
        """
        Get the database schema information.
        
        Returns:
            str: Schema information
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get table info
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema_info = []
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            schema_info.append(f"\nTable: {table_name}")
            schema_info.append("Columns:")
            for col in columns:
                schema_info.append(f"  - {col[1]} ({col[2]})")
                
        conn.close()
        return "\n".join(schema_info)

class HeartDiseaseDBTool(BaseDBTool):
    def __init__(self):
        super().__init__("heart_disease.db")

class CancerDBTool(BaseDBTool):
    def __init__(self):
        super().__init__("cancer.db")

class DiabetesDBTool(BaseDBTool):
    def __init__(self):
        super().__init__("diabetes.db")
