import pandas as pd
import sqlite3
import os
from pathlib import Path

def setup_databases():
    """
    Convert CSV files to SQLite databases.
    """
    # Get the project root directory
    root_dir = Path(__file__).parent.parent.parent
    
    # Create database directory if it doesn't exist
    db_dir = root_dir / "data" / "db"
    db_dir.mkdir(exist_ok=True)
    
    # Setup Heart Disease Database
    heart_df = pd.read_csv(root_dir / "heart.csv")
    conn = sqlite3.connect(db_dir / "heart_disease.db")
    heart_df.to_sql("heart_disease", conn, if_exists="replace", index=False)
    conn.close()
    print("Created heart_disease.db")
    
    # Setup Cancer Database
    cancer_df = pd.read_csv(root_dir / "The_Cancer_data_1500_V2.csv")
    conn = sqlite3.connect(db_dir / "cancer.db")
    cancer_df.to_sql("cancer", conn, if_exists="replace", index=False)
    conn.close()
    print("Created cancer.db")
    
    # Setup Diabetes Database
    diabetes_df = pd.read_csv(root_dir / "diabetes.csv")
    conn = sqlite3.connect(db_dir / "diabetes.db")
    diabetes_df.to_sql("diabetes", conn, if_exists="replace", index=False)
    conn.close()
    print("Created diabetes.db")

if __name__ == "__main__":
    setup_databases()
    print("All databases successfully created!")
