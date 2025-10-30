import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from utility_function import (embed_text_with_gemini, create_opensearch_client, search_similar_qa, build_prompt,get_gemini_response)

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if "conversation" not in st.session_state:
    st.session_state.conversation = []  

st.title("Aurora Skies Airways Assistant")

user_question = st.chat_input("Ask a question...")

if user_question:
    st.session_state.conversation.append(("user", user_question))

    st.markdown(f"🧑 User:\n{user_question}")


    assistant_placeholder = st.empty()
    assistant_placeholder.markdown("🤖 Assistant:\n_Thinking..._")

    opensearch_client = create_opensearch_client()
    google_client = genai.Client(api_key=google_api_key)

    with st.spinner("Analyzing..."):
        embedding = embed_text_with_gemini(user_question, google_client)
        vector = embedding.embeddings[0].values
        similar_context = search_similar_qa(opensearch_client, vector)
        prompt = build_prompt(user_question, similar_context)
        response = get_gemini_response(google_client, prompt)

    answer_text = response.text if hasattr(response, "text") else str(response)
    st.session_state.conversation.append(("assistant", answer_text))
    assistant_placeholder.markdown(f"🤖 Assistant:\n{answer_text}")
    st.stop()
conversation_text = ""
for role, text in st.session_state.conversation:
    prefix = "🧑 User:" if role == "user" else "🤖 Assistant:"
    conversation_text += f"{prefix}\n{text}\n\n"
st.markdown(conversation_text)