# Aurora Skies Airways Assistant
Aurora Skies Airways Assistant is a Streamlit-based chatbot that uses Google Gemini for language understanding and OpenSearch for retrieving relevant FAQ data. It provides context-aware answers to user queries about airline services.

<img width="1365" height="767" alt="image" src="https://github.com/user-attachments/assets/f25bf5fc-3c98-4d47-9516-788924b09453" />
## Tech Stack
1. Streamlit
   For building the interactive chatbot UI.
2. Python
   Core language for the application logic and integration.
3. Google Gemini API
   gemini-embedding-001 for generating vector embeddings of user queries and FAQs.
   gemini-2.0-flash for generating conversational responses.
4. Vector Database - OpenSearch
   Used as a KNN-based vector search engine to store and retrieve FAQ embeddings.
   Index configured with knn_vector type for similarity search.
