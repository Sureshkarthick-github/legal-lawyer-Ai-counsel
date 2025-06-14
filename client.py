import requests
import streamlit as st

def get_openai_response(input_text: str) -> str:
    try:
        response = requests.post(
            "http://localhost:8000/answer/invoke",
            json={'input': {'topic': input_text}}
        )
        response.raise_for_status()  # Check for HTTP errors
        return response.json().get('output', {}).get('content', 'No content received')
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the FastAPI server. Make sure it is running.")
        return "Connection error."
    except requests.exceptions.RequestException as e:
        st.error(f"Request error: {e}")
        return "Request error."
    except KeyError:
        st.error("Unexpected response format from API.")
        return "Invalid response format."

st.title("Legal Lawyer AI Counsel")

input_text = st.text_input("Provide your legal query:")
if input_text:
    output = get_openai_response(input_text)
    st.write(output)
