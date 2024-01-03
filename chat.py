import random
import json

import torch


from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

from db_operations import get_user_full_name,get_score
from api_operations import get_translation,call_youglish_api,generate_chatbot_response



device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"


def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                if tag == "translation":
                    word_to_translate = " ".join(sentence[2:]) 
                    translation = get_translation(word_to_translate)
                    return f"{word_to_translate} means: {translation}"
                if tag == "askName":
                    user_full_name = get_user_full_name()
                    return intent['responses'][0].replace("[username]", user_full_name)
                if tag == "askScore":
                    user_full_name = get_score()
                    return user_full_name
                if tag == "suggestVideo":
                    vocabulary_suggest = " ".join(sentence[2:]) 
                    response = call_youglish_api(vocabulary_suggest)
                    return f'Click <a href="{response}" target="_blank"> {vocabulary_suggest}</a> to get suggest video'
                if tag == "chatGPTprompt":
                    req = " ".join(sentence[2:]) 
                    response = generate_chatbot_response(req)
                    return f'GPT:{response}'
                return random.choice(intent['responses'])
    return "Sorry, I'm not able to understand you .."
if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

# def get_response(msg):
#     sentence = tokenize(msg)
#     X = bag_of_words(sentence, all_words)
#     X = X.reshape(1, X.shape[0])
#     X = torch.from_numpy(X).to(device)

#     output = model(X)
#     _, predicted = torch.max(output, dim=1)

#     tag = tags[predicted.item()]

#     probs = torch.softmax(output, dim=1)
#     prob = probs[0][predicted.item()]
#     if prob.item() > 0.75:
#         for intent in intents['intents']:
#             if tag == intent["tag"]:
#                 return random.choice(intent['responses'])
    
#     return "I do not understand..."