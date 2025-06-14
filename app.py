from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langserve import add_routes
import uvicorn
from dotenv import load_dotenv

# Load environment variables (if needed)
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Law Chatbot",
    version="1.0",
    description="A simple API Server"
)

# Initialize the Ollama LLM with the correct model name
llm = Ollama(model="llama2")

# Define a chat prompt template
prompt1 = ChatPromptTemplate.from_template("Provide me {topic} with 100 words")

# Add routes for LLM and prompt integration
add_routes(
    app, 
    llm, 
    path="/chatbot"
)

add_routes(
    app,
    prompt1 | llm,
    path="/answer"
)

# Run the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
