import streamlit as st
from langdb import get_few_shot_db_chain

def main():
    # Streamlit App Title
    st.title("AtliQ T-Shirts: Database Q&A 👕")
    
    # Get the function to generate SQL queries and fetch results
    query_function = get_few_shot_db_chain()
    
    # User input
    question = st.text_input("Enter your question:")
    
    if st.button("Get SQL Query and Result"):
        if question:
            try:
                result = query_function(question)  # Get query result
                st.success("Generated SQL Query:")
                st.code(result["query"], language="sql")
                
                st.success("Query Result:")
                st.write(result["data"])
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
