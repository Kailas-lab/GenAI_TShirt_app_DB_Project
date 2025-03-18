from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langchain.utilities import SQLDatabase
import re
from langchain.prompts import PromptTemplate
from langchain.chains import create_sql_query_chain
from sklearn.feature_extraction.text import TfidfVectorizer
from langchain.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from few_shots import few_shots
import numpy as np
from langchain.embeddings.base import Embeddings # type: ignore

api_key = 'AIzaSyDXzd_RQigQ4MXNzefE-o1B27ymhIYka7k'

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.2)


def get_few_shot_db_chain():
    print("Initializing database connection...")  # Debugging step
    db_user = "root"
    db_password = "root"
    db_host = "localhost"
    db_name = "atliq_tshirts"

    try:
        db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}", sample_rows_in_table_info=3)
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None  # Return None if DB connection fails

    # Embedding setup (Placeholder)
    class SimpleEmbeddings(Embeddings):
        def embed_documents(self, texts):
            return np.random.rand(len(texts), 26).tolist()

        def embed_query(self, text):
            return np.random.rand(26).tolist()

    embeddings = SimpleEmbeddings()

    try:
        vectorstore = Chroma.from_texts(
            [" ".join(str(value) for value in example.values()) for example in few_shots],
            embeddings,
            metadatas=few_shots,
            persist_directory="./chroma_db"
        )
        vectorstore.persist()
    except Exception as e:
        print(f"Vectorstore initialization failed: {e}")
        return None  # Return None if vectorstore fails

    example_selector = SemanticSimilarityExampleSelector(vectorstore=vectorstore, k=2)

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate(
            input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
            template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
        ),
        prefix=_mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"],
    )

    new_chain = create_sql_query_chain(llm, db, prompt=few_shot_prompt)

    def fun2(question):
        print(f"Processing question: {question}")  # Debugging step
        try:
            sql_response = new_chain.invoke({"question": question})
            print(f"SQL Response: {sql_response}")  # Debugging step

            sql_query = re.search(r"SELECT .*", sql_response, re.DOTALL)
            if sql_query:
                extracted_query = sql_query.group(0)
                print(f"Extracted SQL Query: {extracted_query}")  # Debugging step

                result = db.run(extracted_query)
                print(f"Query Result: {result}")  # Debugging step

                return {"query": extracted_query, "data": result}

            return {"query": None, "data": "Failed to extract query"}
        except Exception as e:
            print(f"Error executing query: {e}")
            return {"query": None, "data": f"Error: {e}"}

    print("Returning fun2 function...")  # Debugging step
    return fun2





    



