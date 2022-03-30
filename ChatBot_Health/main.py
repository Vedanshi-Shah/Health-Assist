from turtle import update
from fpdf import FPDF
import Constants as keys
from telegram.ext import *
from telegram import *
import requests
import json
import requests
from bot import *
from firebase import firebase
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size = 11)
firebase = firebase.FirebaseApplication('https://healthassist-aed4f-default-rtdb.asia-southeast1.firebasedatabase.app/', None)
import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate('healthAssistFirestore.json')
firebase_admin.initialize_app(cred, 
{
'databaseURL': 'https://HealthAssist.firebaseio.com/'
})
db = firestore.client()
doc_ref_curr = db.collection(u'Current Disease')
doc_ref_his=db.collection(u'userHistory')
print("Bot started")
names_intents = {
    "intents_initial" : "Major Symptom",
    "intents_intermidiate" : "Exact Location or Type of Pain",
    "intents_final" : "Accompanying Symptoms"
}
trusted_sources = ["mayoclinic","webmd","clevelandclinic","medlineplus","nhs","clevelandclinic","ncbi","niddk"]
univ_intents=dict()
univ_specific = dict()
univ_user_diseases_suspect = dict()
univ_user_history = dict()
univ_que_ans_dict = dict()

tag=0
doctors = json.loads(open('doctors_info.json').read())
disease_to_doctor = json.loads(open('disease_to_doctor.json').read())
# extract chat_id based on the incoming object
def get_links(disease):
    trusted_sources = ["mayoclinic","webmd","clevelandclinic","medlineplus","nhs","clevelandclinic","ncbi","niddk"]
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

def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]
    return chat_id

def send_pdf(chat_id):
    url = "https://api.telegram.org/bot" + str(keys.API_KEY) + "/sendDocument?chat_id="+ str(chat_id) +""
    payload = {}
    files = [
        ('document', open('Assessment.pdf','rb'))
    ]
    headers= {}
    response = requests.request("POST", url, headers=headers, data = payload, files = files)
    print(response.text.encode('utf8'))

def send_links(bot_message,bot_chatID):
    message = ""
    bot_token = keys.API_KEY
    for key in bot_message.keys():
        message += key+" : "
        for i in range(len(bot_message[key])):
            message += str(i+1) + ". "+bot_message[key][i] + "\n" 
            send_text = 'https://api.telegram.org/bot' + str(bot_token) + '/sendMessage?chat_id=' + str(bot_chatID) + '&parse_mode=Markdown&text=' + message
            response = requests.get(send_text)
            message = ""   
    print(response.json())

def send_contacts(user_specific,id):
    bot_token = keys.API_KEY
    message = "Doctors Required for particular diseases suspected : \n"
    for key in user_specific:
        message += key[0] + disease_to_doctor[key[0]]
        send_text = 'https://api.telegram.org/bot' + str(bot_token) + '/sendMessage?chat_id=' + str(id) + '&parse_mode=Markdown&text=' + message
        response = requests.get(send_text)
        message=""
    for key in doctors.keys():
        message = "The contact numbers of " + key + " are listed below : \n"
        for nums in doctors[key].keys():
            message += nums + doctors[key][nums]
            send_text = 'https://api.telegram.org/bot' + str(bot_token) + '/sendMessage?chat_id=' + str(id) + '&parse_mode=Markdown&text=' + message
            response = requests.get(send_text)
            message=""
def sample_responses(input_text,update,context):
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    user_message = str(input_text).lower()
    tag = 0
    res = ""
    id=get_chat_id(update,context)
    print(univ_intents[id])
    
    # print(general_done(univ_intents[id]))
    if(general_done(univ_intents[id]) == False or id in univ_user_diseases_suspect.keys()):
        if (general_done(univ_intents[id]) == False):
            res=bot_general(univ_intents[id],user_message,univ_que_ans_dict[id])
            if (general_done(univ_intents[id]) == True):
                tag = 1
        if (id in univ_user_diseases_suspect.keys()) and (general_done(univ_intents[id])):
            if (univ_user_diseases_suspect[id] == {}):
                univ_user_diseases_suspect[id] = get_suspects(univ_intents[id])
            if tag == 1:
                res = bot_specific(univ_user_diseases_suspect[id],univ_specific[id],res,univ_intents[id],univ_que_ans_dict[id])
                tag = 0
            else:
                res = bot_specific(univ_user_diseases_suspect[id],univ_specific[id],user_message,univ_intents[id],univ_que_ans_dict[id])
            if (univ_user_diseases_suspect[id] == {}):
                user_message=""
                del univ_user_diseases_suspect[id]
    print(univ_que_ans_dict[id])
    if(user_message=="" or res==""):
        doc=doc_ref_his.stream()
        flag=0
        user_hist=univ_user_history[id]
        for i in doc:
            if(i.id==str(id)):
                flag=1
                user_hist=i.to_dict()
                break
        if(flag==1):
            univ_user_history[id]={
                "email":user_hist['email'],
                "Name" : user_hist['Name'], 
                "Age" : univ_user_history[id]['Age'],     
                "height" : user_hist['height'], 
                "Weight" : univ_user_history[id]['Weight'], 
                "gender" : user_hist['gender'],  
                "Diet" : user_hist['Diet'], 
                "Alcohol" : univ_user_history[id]['Alcohol'],
                "StressedLifestyle" :univ_user_history[id]['StressedLifestyle'],
                "SimilarHistory":univ_user_history[id]['SimilarHistory']
            }
            res=bot_history(univ_user_history[id],univ_specific[id],univ_intents[id],user_message)
        else:
            res=bot_history_initial(univ_user_history[id],univ_specific[id],univ_intents[id],user_message)
        if res == "Thank You!":
            
            univ_specific[id]=sorted(univ_specific[id], key=lambda x: x[1], reverse=True)
            res = "We have completed the analysis of your symptoms. You are sustected to have : \n"
            count = 0
            res_user = "The diseases suspected are - "
            for disease in univ_specific[id]:
                res += (disease[0].capitalize() + "\n")
                res_user += (disease[0].capitalize() + " ")
                count += 1
                if count == 3:
                    break
            res += "Some information related to these diseases is shared below"
            univ_que_ans_dict[id]['Final Suspected Diseases'] = res_user
            print(univ_que_ans_dict[id])
            print(univ_intents[id])
            pdf.cell(120,10,txt="Analysis of the Current Disease", ln=1, align='R')
            for key in univ_user_history[get_chat_id(update,context)].keys():
                text = key+" : "+univ_user_history[get_chat_id(update,context)][key]
                pdf.cell(20, 10, txt = text, ln = 1, align = 'L')
            questions = univ_que_ans_dict[get_chat_id(update,context)]
            for key in questions.keys():
                if type(questions[key]) != list:
                    text = key+" : "+questions[key]
                else:
                    for i in range(len(questions[key])):
                        if i == 0:
                            text = names_intents[key]+" : "+questions[key][i]
                        else:
                            text += " "+questions[key][i]
                pdf.cell(200, 10, txt = text, ln = 1, align = 'L')
            pdf.output("Assessment.pdf")
            send_pdf(id)
            link = {}
            count = 0
            print(univ_specific[id])
            for disease in univ_specific[id]:
                print(disease)
                link[disease[0]] = get_links(disease[0])
                count += 1
                if count == 3:
                    break
            send_links(link,id)
            send_contacts(univ_specific[id],id)
            data={
                u'Chat Id':str(get_chat_id(update,context)),
                u'Current Diseases':str(univ_specific[get_chat_id(update,context)]),
                u'Question Answer':str(univ_que_ans_dict[get_chat_id(update,context)]),
                u'Symptoms':str(univ_intents[get_chat_id(update,context)])
            }
            doc_ref_curr.document(str(id)).set(data)
            univ_user_history[id]['chatId']=str(id)
            doc_ref_his.document(str(id)).set(univ_user_history[id])
            
            del univ_intents[get_chat_id(update,context)]
            del univ_specific[get_chat_id(update,context)]
            del univ_user_history[get_chat_id(update,context)]
            del univ_que_ans_dict[get_chat_id(update,context)]
    return res

def start_command(update, context):
    update.message.reply_text('Type something to get started')

def help_command(update, context):
    update.message.reply_text('If you need help ask on google')

def handle_messsage(update, context):
    text = str(update.message.text).lower()
    id=get_chat_id(update,context)
    if id not in univ_intents.keys():
        univ_intents[id]=[]
        univ_specific[id] = []
        univ_user_diseases_suspect[id] = dict()
        univ_user_history[id] = {
            "email":"",
            "Name" : "", 
            "Age" : "",     
            "height" : "", 
            "Weight" : "", 
            "gender" : "",  
            "Diet" : "" , 
            "Alcohol" : "",
            "StressedLifestyle" :"",
            "SimilarHistory":""
        }
        univ_que_ans_dict[id] = {}
    response = sample_responses(text,update,context)
    
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