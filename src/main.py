import streamlit as st
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.tools.agent import MedicalAgent

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(page_title="Medical AI Assistant", layout="wide")
    
    st.title("🏥 Medical AI Assistant")
    st.markdown("""
    Welcome to the Medical AI Assistant! This system can:
    - Answer questions about heart disease, cancer, and diabetes data
    - Provide general medical information and knowledge
    """)
    
    # Initialize the agent
    if 'agent' not in st.session_state:
        st.session_state.agent = MedicalAgent()
    
    # Create tabs
    tab1, tab2 = st.tabs(["Chat Interface", "About"])
    
    with tab1:
        # Chat interface
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User input
        if prompt := st.chat_input("Ask your medical question..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.agent.process_query(prompt)
                    st.markdown(response)
                    
            # Add AI response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

    with tab2:
        st.markdown("""
        ### About This System
        
        This AI assistant can help you with:
        
        1. **Medical Data Analysis**
           - Statistics about heart disease patients
           - Cancer data analysis
           - Diabetes patient information
        
        2. **General Medical Knowledge**
           - Disease symptoms and causes
           - Treatment information
           - Prevention strategies
        
        ### Example Questions
        
        Data Analysis:
        - "What is the average age of heart disease patients?"
        - "Show me the distribution of cancer types in the dataset"
        - "What percentage of diabetes patients are over 50?"
        
        Medical Knowledge:
        - "What are the early symptoms of heart disease?"
        - "How is breast cancer diagnosed?"
        - "What are the risk factors for type 2 diabetes?"
        """)

if __name__ == "__main__":
    main()
