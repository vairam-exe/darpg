import os
import google.generativeai as genai
import PIL.Image
import streamlit as st
import yaml

# Load API Key from configuration file
with open("config.yaml", "r") as f:
    config = yaml.full_load(f)

# Set up the API key for Google Generative AI
api_key = config['gemini']['api_key']
os.environ['GOOGLE_API_KEY'] = api_key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Load the input image
input_image = PIL.Image.open('CPGRAMS.jpg')

# Select the model to be used in the app
model = genai.GenerativeModel('gemini-pro-vision')

# Initiate the chat session
chat = model.start_chat(history=[])

def get_gemini_response(question):
    """Generate a response from the Gemini model based on the input question and image."""
    response = model.generate_content([question, input_image])
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("DARPG Chatbot")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input for questions
user_input = st.text_input("How can I help you: ", key="input")
submit_button = st.button("Submit")

if submit_button and user_input:
    # Get response from the Gemini model
    response = get_gemini_response(user_input)

    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", user_input))
    st.subheader("Answer is")
    
    # Display the response
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Optional: Uncomment to display the chat history
# st.subheader("Chat History")
# for role, text in st.session_state['chat_history']:
#     st.write(f"{role}: {text}")
