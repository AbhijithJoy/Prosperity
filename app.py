import streamlit as st
import requests
import time

# Use the model endpoint
api_url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
api_key = "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"

def query_huggingface(payload):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(api_url, headers=headers, json=payload)
    
    # Check if the model is still loading
    if response.status_code == 503:
        result = response.json()
        st.write(f"Model is loading, please wait for {result['estimated_time']} seconds.")
        time.sleep(result['estimated_time'])
        response = requests.post(api_url, headers=headers, json=payload)
    
    return response.json()

# Streamlit UI
st.title("Prosperity Chatbot")

user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        # Send user input to Hugging Face
        output = query_huggingface({"inputs": user_input})
        
        # Debug: Show the raw API response
        #st.write("API Response:", output)
        
        # Attempt to display the bot's response
        if isinstance(output, list) and len(output) > 0:
            bot_response = output[0].get("generated_text", "Sorry, I couldn't generate a response.")
            st.write("Bot:", bot_response)
        else:
            st.write("Bot: Sorry, I couldn't generate a response.")


