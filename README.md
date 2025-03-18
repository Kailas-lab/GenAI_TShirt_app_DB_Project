**AtliQ Tees: Talk to a Database**

This is an end to end LLM project based on Google gemini and Langchain. We are building a system that can talk to MySQL database. User asks questions in a natural language and the system generates answers by converting those questions to an SQL query and then executing that query on MySQL database. AtliQ Tees is a T-shirt store where they maintain their inventory, sales and discounts data in MySQL database. A store manager will may ask questions such as,

How many white color Adidas t shirts do we have left in the stock?

How much sales our store will generate if we can sell all extra-small size t shirts after applying discounts? The system is intelligent enough to generate accurate queries for given question and execute them on MySQL database


**Project Highlights:**

AtliQ Tees is a t shirt store that sells Adidas, Nike, Van Heusen and Levi's t shirts
Their inventory, sales and discounts data is stored in a MySQL database
We will build an LLM based question and answer system that will use following,
Google gemini
fake embeddings
Streamlit for UI
Langchain framework
Chromadb as a vector store
Few shot learning
In the UI, store manager will ask questions in a natural language and it will produce the answers