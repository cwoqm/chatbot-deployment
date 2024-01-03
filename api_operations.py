#api_operations.py
from bs4 import BeautifulSoup
import requests

# Your existing code for get_response function

# def get_translation(word, target_language):
#     api_url = f"https://api.mymemory.translated.net/get?q={word}&langpair=en|{target_language}"
#     response = requests.get(api_url)
#     translation_data = response.json()
#     translated_text = translation_data.get("responseData", {}).get("translatedText", "").lstrip('*-: ').lower()
#     target_language =target_language.lower() 
#     if target_language == translated_text:
#         return f"Translation not found"
#     else:
#         return translated_text

def get_translation(word):
    api_url = f"https://translate.googleapis.com/translate_a/single?client=dict-chrome-ex&sl=en&tl=vi&hl=en-US&dt=t&dt=bd&dj=1&source=bubble&q={word}"
    response = requests.get(api_url)
    translation_data = response.json()
    translated_text = translation_data["sentences"][0]["trans"]
    return translated_text

# def call_youglish_api(query, language):
#     # api_url = "https://youglish.com/pronounce/{query}/{language}?"
#     api_url = "https://youglish.com/pronounce/comment/english"
#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()
#         data = response.json()
#         print(f"Response {response.raise_for_status()},data={data} ")
#         return data
#     except requests.exceptions.RequestException as e:
#         print(f"Error making YouGlish API request: {e}")

import openai

def call_youglish_api(query):
    link = f'https://youglish.com/pronounce/{query}/english/'
    return link

openai.api_key = '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'

def generate_chatbot_response(user_input):
    # Create a chat completion request
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You will be provided with statements, and your task is to convert them to standard English."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0.7,
        max_tokens=64,
        top_p=1
    )
    chatbot_response = response['choices'][0]['message']['content'].strip()
    return chatbot_response