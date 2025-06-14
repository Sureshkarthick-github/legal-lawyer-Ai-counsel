import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import time

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a legal AI assistant. Answer only legal queries. Categorize each query as Criminal Law, Family Law, Civil Law, Corporate Law, or Constitutional Law. If a question is unrelated to law, politely decline to answer."),
    ("user", "Question: {question}")
])


llm = Ollama(model="llama3.2")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

def classify_law_category(response):
    categories = ["Criminal Law", "Family Law", "Civil Law", "Corporate Law", "Constitutional Law"]
    for category in categories:
        if category.lower() in response.lower():
            return category
    return "Others"


st.set_page_config(page_title="Legal AI Chatbot", page_icon="⚖️", layout="wide")

st.title("⚖️ Legal AI Counsel 🤖")

with st.sidebar:
    st.header("Chat Settings")
    st.markdown("This chatbot provides legal guidance based on queries.")
    st.markdown("---")
    st.subheader("📜 Chat History")

 
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


    for idx, (query, reply, category) in enumerate(reversed(st.session_state.chat_history)):
        with st.expander(f"**{category}**: {query[:30]}...", expanded=False):
            st.markdown(f"**User:** {query}")
            st.markdown(f"**AI:** {reply}")


input_text = st.text_input("💬 Ask your legal question:", key="input")

if input_text:
    with st.spinner("Analyzing your question...💬"):
        response = chain.invoke({"question": input_text})
        law_category = classify_law_category(response)
        
        if "law" in response.lower() or "legal" in response.lower():
            st.session_state.chat_history.append((input_text, response, law_category))
            st.markdown("## 🧾 Case Summary")

            st.markdown(f"### 🔖 Category: `{law_category}`")

            st.markdown("### 📜 Legal Solution")
            st.write(response)

            st.markdown("### 👨‍⚖️ Suggested Lawyer Contacts")
            st.markdown("""
            - **Adv. Rajesh Kumar** — Criminal Law Specialist, Chennai (📞 +91-9876543210)  
            - **Adv. Meera Sharma** — High Court Advocate, Delhi (📞 +91-9876501234)  
            - **Adv. Anil Verma** — Legal Aid Services, Mumbai (📞 +91-9000000001)  
            """)
        else:
            st.warning("❌ This chatbot only answers legal questions.")
