import streamlit as st
import os
import getpass
from groq import Groq

# --- Groq API Key Setup ---
# This will re-prompt for the API key if not already set in the environment
# For Streamlit deployment, it's best to handle this via secrets management
if "api" not in os.environ:
    os.environ["api"] = getpass.getpass("Enter your Groq API Key:")

client = Groq(api_key=os.environ.get("api"))

# --- Knowledge Base ---
knowledge_base=[
    "Capcity of production 500",
    "we have in hand invetory 50000, remaning we need to produce",
    "you need to contact 1 pm am to 5 pm for customer support",
    "you can call hr for job related query, hr@sns.com"
]

context = " ".join(knowledge_base)

# --- Streamlit App --- 
st.title("Groq-powered Knowledge Base Chatbot")
st.write("Ask a question based on the provided knowledge base.")

user_query = st.text_input("Your question:", "can we deliver 60000 units today?")

if st.button("Get Answer"):
    if user_query:
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Use the provided context to answer questions."
                    },
                    {
                        "role": "user",
                        "content": f"{context}. Based on this context, {user_query}"
                    }
                ],
                model="llama-3.1-8b-instant", # Using the model that worked previously
                temperature=0
            )
            st.write("**Response:**")
            st.info(chat_completion.choices[0].message.content)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.warning("Please ensure your Groq API key is correctly entered and the model 'llama-3.1-8b-instant' is still available.")
    else:
        st.warning("Please enter a question.")
