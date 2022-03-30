import random
import json
from turtle import update
import Constants as keys
from telegram.ext import *
from telegram import *
import torch
from model import NeuralNet
from bs4 import BeautifulSoup
import requests
import json
from urllib.request import Request, urlopen
from nltk_utils import bag_of_words, tokenize

print("Bot started")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]
    return chat_id

def get_links(disease):
     trusted_sources = ["mayoclinic","webmd","clevelandclinic","medlineplus","nhs","clevelandclinic","ncbi","niddk","healthline","nimh"]
     names = disease.split(" ")
     link = "https://www.google.dz/search?q="
     for i in range(len(names)):
          link += names[i]
          if i != len(names)-1:
               link+="+"
     req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
     soup = BeautifulSoup((urlopen(req)).read())
     links = soup.findAll("a")
     print(type(links))
     final_links = []
     count = 0
     for link in links:
          l = link["href"]
          arr = l.split("?")
          if arr[0] == "/url":
               k = l.split(".")
               for site in trusted_sources:
                    if site in k:
                         path = "https://www.google.dz"+l
                         final_links.append(path)
                         trusted_sources.remove(site)
                         count += 1
          if count == 2:
               break
     return final_links

def send_links(bot_message,bot_chatID):
     final = ""
     links = get_links(bot_message)
     bot_token = keys.API_KEY
     i = 0
     for key in links:
          final += key + "\n" 
          send_text = 'https://api.telegram.org/bot' + str(bot_token) + '/sendMessage?chat_id=' + str(bot_chatID) + '&parse_mode=Markdown&text=' + final
          response = requests.get(send_text)
          final = ""   
          i += 1
     print(response.json())

get_links_of = ["anxiety", "depression", "schizophrenia"]

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Mentee"

def get_response(msg,update,context):
     id = get_chat_id(update, context)
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
                    if intent["tag"] in get_links_of:
                         send_links(intent["tag"],id)
                    return random.choice(intent['responses'])
     else:
          return "I do not understand..."

def start_command(update, context):
     update.message.reply_text('Type something to get started')

def help_command(update, context):
     update.message.reply_text('If you need help ask on google')

def handle_messsage(update, context):
     text = str(update.message.text).lower()
     response = get_response(text,update,context)

     update.message.reply_text(response)

def error(update, context):
     print(f"Update {update} caused error {context.error}")

def main():
     updater = Updater(keys.API_KEY, use_context=True)
     dp = updater.dispatcher

     dp.add_handler(CommandHandler("start", start_command))
     dp.add_handler(CommandHandler("help", help_command))
     dp.add_handler(MessageHandler(Filters.text, handle_messsage))
     dp.add_error_handler(error)
     updater.start_polling()
     updater.idle() 
     
main()