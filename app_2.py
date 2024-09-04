import streamlit as st
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_query = data['queryResult']['queryText']

    # Call to Hugging Face API
    hf_api_url = 'https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill'
    headers = {'Authorization': 'Bearer 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'}
    response = requests.post(hf_api_url, headers=headers, json={'inputs': user_query})
    result = response.json()

    # Return the LLM response to Dialogflow
    return jsonify({
        'fulfillmentText': result.get('generated_text', 'Sorry, I did not understand that.')
    })

if __name__ == '__main__':
    app.run(port=5000)

