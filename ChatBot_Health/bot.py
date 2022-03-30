import random
import pickle
import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import copy
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('chatbot_model.h5')

greeting_intent = ["greeting"]
intents_initial = ["AbdomenPain","ChestPain"]
intents_intermidiate = ["UpRightAbdPain","CentralAbdPain","AroundCentAbdPain","LowerAbdPain","LeftShoulderPain","BurningPain","LocalisedPain","Breating"]
intents_final = ["Vomit","Jaundice","Weight","Diarreha","Fever","Nausea","No","Uneasiness", "Sweating"]
intents_yesNo = ["Yes","No"]
#To make a disease wise sevearity list.

disease_abdomen_classification = {
    "UpRightAbdPain" : ["Cholecystitis","Gall Stone Obstruction", "Hepatitis", "Amoebic Abscess"], 
    "CentralAbdPain" : ["Gasteric Ulcer", "Pancreatitis","Colitis"],
    "AroundCentAbdPain" : ["Kidney Stone","Peretonitis","Gastroenteritis"],#More Diseases to Add
    "LowerAbdPain" : ["Appendicitis"]              
}#More Diseases to Add

disease_to_symptoms_intents_chest = {
    "Ischemia" : ["ChestPain","LeftShoulderPain","Sweating","Uneasiness","Weight","StressedLifestyle"],
    "Reflux Oesophagitis" : ["BurningPain" ,"Food", "Regurgitation","Diet","SimilarHistory"],
    "Pleuritis" : ["LocalisedPain", "Fever","SimilarHistory"],
    "Rib Fracture" : ["ChestPain","LocalisedPain"],
    "Chostochondritis" : ["ChestPain","Breathing"]
}

disease_chest_classification = {
    "LeftShoulderPain" : ["Ischemia"], 
    "BurningPain" : ["Reflux Oesophagitis"],
    "LocalisedPain" : ["Pleuritis","Rib Fracture"],#More Diseases to Add
    "Breathing" : ["Chostochondritis"]              
}

disease_to_symptoms_intents = {
    "Cholecystitis" : ["UpRightAbdPain","Fever","Vomit","Middle-Age","Fat"],#Age, #Weight, #Gender {Fat , Female, Fertile}
    "Gall Stone Obstruction" : ["UpRightAbdPain","Vomit","Jaundice","Middle-Age","Fat"], #Age, #Weight, #Gender {Fat , Female, Fertile}
    "Hepatitis" : ["UpRightAbdPain","Jaundice","SimilarHistory"],#History of Jaundice
    "Amoebic Abscess" : ["UpRightAbdPain","Fever","Jaundice"],#History of Dysentry
    "Gasteric Ulcer" : ["CentralAbdPain","Weight","StressedLifestyle","Alcohol"], #Stressed, #Spiecy, #Alcohol
    "Pancreatitis" : ["CentralAbdPain","Fever","Vomit","Alcohol"], #Alcoholism, #Trauma
    "Kidney Stone" : ["AroundCentAbdPain","SimilarHistory"], #More Symptomes to Add, #History of Similar Pain
    "Peretonitis" : ["AroundCentAbdPain","Vomit","Fever","Weight"],
    "Gastroenteritis" : ["AroundCentAbdPain","Fever","Vomit","Diarrhea"],#Contaminated Food/ Uncooked Food or Water
    "Colitis" : ["CentralAbdPain","SimilarHistory"],#To add Jaudice and Dysentry #Similar Complaints
    "Appendicitis" : ["LowerAbdPain","Fever","Vomit","SimilarHistory"] #Similar Complaints 
}
disease_to_symptoms_particular = {
    "Cholecystitis" : ["Is pain radiation to Right Shoulder?? (Yes/No)"],#Age, #Weight, #Gender {Fat , Female, Fertile}
    "Gall Stone Obstruction" : ["Is the pain Colicky? (It comes and it goes) (Yes/No)"], #Age, #Weight, #Gender {Fat , Female, Fertile}
    "Gasteric Ulcer" : ["Does the pain start after you have a meal and subsides after the stomach is empty??(Yes/No)"], #Stressed, #Spiecy, #Alcohol
    "Pancreatitis" : ["Does the pain rediate to back??(Yes/No)"], #Alcoholism, #Trauma
    "Kidney Stone" : ["Did you ever notice blood in your urine? (Yes/No)","Did you notice any fine granule like particles passing through urine? (Yes/No)"], #More Symptomes to Add, #History of Similar Pain
    "Peretonitis" : ["Do you feel like you are having palpations?(Yes/No)"],
    "Gastroenteritis" : ["Are you having generalised pain in stomach all the time?(Yes/No)", "Have you consumed some uncooked food or do you fell like you have drank contaminated water recently?(Yes/No)"],#Contaminated Food/ Uncooked Food or Water
    "Colitis" : ["Are you having Dysentry?(Yes/No)"],#To add Jaudice and Dysentry #Similar Complaints
    "Appendicitis" : ["Does the pain radiate from front to back??(Yes/No)"] #Similar Complaint
}

disease_to_symptoms_particular_chest = {
    "Ischemia" : ["Do you have difficulty in breating?(Yes/No)","Do you feel heaviness?(Yes/No)"],
    "Reflux Oesophagitis" : ["Does the regurgitation of food happens after food intake?(Yes/No)"],
    "Rib Fracture" : ["Is there a localised swelling over the area of pain?(Yes/No)","Does the pain increase with the movement of ribs?(Yes/No)"],
    "Chostochondritis" : ["Is the pain near or front of ribs?(Yes/No)"]
}

general_history = {
    "email":"Please enter your registered email id",
    "Name" : "What is your name?", 
    "Age" : "What is your age?",     
    "height" : "What is your height?(Provide a approx figure in cms)(only numbers)", 
    "Weight" : "What is your weight?(In Kg)(only numbers)", 
    "gender" : "Gender ?",  
    "Diet" : "Are you Vegetarian or Non-Vegeterain?" , 
    "Alcohol" : "Do you consume alcohol? (Yes/No)",
    "StressedLifestyle" : "Have you been stressed thsee days? (Yes/No)",
    "SimilarHistory" : "Have you ever observed similar symptoms before? (Yes/No)",
    
}
history = {
    "email":"",
    "Name" : "", 
    "Age" : "",     
    "height" : "", 
    "Weight" : "", 
    "gender" : "",  
    "Diet" : "" , 
    "Alcohol" : "",
    "StressedLifestyle" :"",
    "SimilarHistory":"",

}

names_intents = {
    "intents_initial" : "Major Symptom",
    "intents_intermidiate" : "Exact Location or Type of Pain",
    "intents_final" : "Accompanying Symptoms"
}

history_in_use = ["Age","Weight","SimilarHistory","Alcohol","StressedLifestyle"]
current_question = ""

#Cleaning up the sentence.
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

#Making bag of words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]* len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

#Predict Class
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    EROOR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > EROOR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse = True)
    return_list = []
    #return_list.append({'intent':classes[results[0][0]],'probability':str(results[0][1])})
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability':str(r[1])})
    
    return return_list

def get_response(intents, intents_json): 
  result = []
  list_of_intents = intents_json['intents']
  for i in list_of_intents:
      if i['tag'] == intents[0]['intent']:
          result = random.choice(i['responses'])
          break
  return result

def get_response_premeditated(intents, intents_json):
  result = []
  list_of_intents = intents_json['intents']
  for i in list_of_intents: 
    if i['tag'] == intents[0]['intent'] and i not in intents_yesNo:
      result = i["responses"][0]
      break
  return result

def get_intents_yesNo(statements):
    res = ""
    recognized_intent = predict_class(statements)
    if recognized_intent[0]['intent'] in intents_yesNo:
            res = recognized_intent[0]['intent']
    return res

def get_intents(statements, user_intents,user_ques):
    responses = ""
    arr_ans = statements.split(".")
    for answer in arr_ans:
        recognized_intent = predict_class(answer)
        print(recognized_intent)
        if recognized_intent == []:
            return responses
        for i in range(len(recognized_intent)):
            if recognized_intent[i]['intent'] in  intents_initial:
                if 'intents_initial' not in user_ques.keys():
                    user_ques['intents_initial'] = [answer]
                else:
                    user_ques['intents_initial'].append(answer)
            if recognized_intent[i]['intent'] in  intents_intermidiate:
                if 'intents_intermidiate' not in user_ques.keys():
                    user_ques['intents_intermidiate'] = [answer]
                else:
                    user_ques['intents_intermidiate'].append(answer)
            if recognized_intent[i]['intent'] in  intents_final:
                if 'intents_final' not in user_ques.keys():
                    user_ques['intents_final'] = [answer]
                else:
                    user_ques['intents_final'].append(answer)      
            if recognized_intent[i]['intent'] in greeting_intent:
                responses = get_response(recognized_intent,intents)
                break
            elif recognized_intent[i]['intent'] in intents_yesNo:
                user_intents.append(recognized_intent[i]['intent'])
                continue
            else:
                user_intents.append(recognized_intent[i]['intent'])
                responses = get_response_premeditated(recognized_intent,intents)
            print(user_ques)
    return responses

def get_suspects(user_intents):
    suspects_diseases = {}
    if "AbdomenPain" in user_intents:
        for intent in user_intents:
            for disease in disease_to_symptoms_intents:
                if intent in disease_to_symptoms_intents[disease] and disease in suspects_diseases:
                    suspects_diseases[disease] += 1
                elif intent in disease_to_symptoms_intents[disease] and disease not in suspects_diseases:
                    suspects_diseases[disease] = 1
        return suspects_diseases
    elif "ChestPain" in user_intents:
        for intent in user_intents:
            for disease in disease_to_symptoms_intents_chest:
                if intent in disease_to_symptoms_intents_chest[disease] and disease in suspects_diseases:
                    suspects_diseases[disease] += 1
                elif intent in disease_to_symptoms_intents_chest[disease] and disease not in suspects_diseases:
                    suspects_diseases[disease] = 1
        return suspects_diseases

def general_done(user_intents):
    initial = False
    intermidiate = False
    final = False
    for intent in user_intents:
        if intent in intents_initial:
            initial = True
        elif intent in intents_intermidiate:
            intermidiate = True
        elif intent in intents_final:
            final = True
    if (final and initial and intermidiate):
        return True
    return False

def bot_general(user_intents, answer,user_ques):
    response = get_intents(answer, user_intents,user_ques)
    # print(response)
    # print(user_intents)
    if general_done(user_intents):
        return ""
    return response

def questions_specific(disease_to_symptoms, key, user_answers):
    res = ""
    if key in disease_to_symptoms.keys():
        for question in disease_to_symptoms[key]:
            if question not in user_answers.keys():
                res = question
                return res
    return res

def bot_specific(user_suspect_diseases,user_specific,answer,user_intents,user_answers):
    res = ""
    arr = []
    global current_question
    if "AbdomenPain" in user_intents:
        if answer == "":
            for key in user_suspect_diseases.keys():
                user_specific.append((key,user_suspect_diseases[key]))
                res = questions_specific(disease_to_symptoms_particular, key, user_answers)
                if res != "":
                    current_question = res
                    break
                else:
                    arr.append(key)
        else:
            sol = get_intents_yesNo(answer)
            user_answers[current_question] = sol
            if sol == "Yes":
                user_specific[len(user_specific)-1] = (user_specific[len(user_specific)-1][0],user_specific[len(user_specific)-1][1]+5)
            for key in user_suspect_diseases.keys():
                tag = 0
                for tup in user_specific:
                    if key == tup[0]:
                        tag = 1
                        break
                if tag == 0:
                    user_specific.append((key,user_suspect_diseases[key]))
                res = questions_specific(disease_to_symptoms_particular, key, user_answers)
                if res != "":
                    current_question = res
                    break
                else:
                    arr.append(key)
    elif "ChestPain" in user_intents:
        if answer == "":
            for key in user_suspect_diseases.keys():
                user_specific.append((key,user_suspect_diseases[key]))
                res = questions_specific(disease_to_symptoms_particular_chest, key, user_answers)
                if res != "":
                    current_question = res
                    break
                else:
                    arr.append(key)
        else:
            sol = get_intents_yesNo(answer)
            print(user_suspect_diseases)
            user_answers[current_question] = sol
            if sol == "Yes":
                user_specific[len(user_specific)-1] = (user_specific[len(user_specific)-1][0],user_specific[len(user_specific)-1][1]+5)
            for key in user_suspect_diseases.keys():
                tag = 0
                for tup in user_specific:
                    if key == tup[0]:
                        tag = 1
                        break
                if tag == 0:
                    user_specific.append((key,user_suspect_diseases[key]))
                res = questions_specific(disease_to_symptoms_particular_chest, key, user_answers)
                if res != "":
                    current_question = res
                    break
                else:
                    arr.append(key)
    for i in arr:
        del user_suspect_diseases[i]
    return res

def bot_history(user_history,user_specific,user_intent,answer):
    print(user_history)
    res = ""
    i=0
    if answer == "":
        for k in user_history.keys():
            if k in history_in_use:
                if(user_history[k]==""):
                    res=general_history[k]
                    break
    else:
        keys=list(user_history.keys())
        tag=0
        i = 0
        if "AbdomenPain" in user_intent:
            for i in range(len(keys)-1):
                if keys[i] in history_in_use:
                    if(user_history[keys[i]]==""):
                        user_history[keys[i]]=answer
                        for k in keys:
                            if(user_history[k]==""):
                                res=general_history[k]
                                break
                        
                        # res=general_history[keys[i+1]]
                        if keys[i] in history_in_use:
                            if keys[i] == "Age":
                                if int(answer)>30 and int(answer)<60:
                                    for j in range(len(user_specific)):
                                        if "Middle-Age" in disease_to_symptoms_intents[user_specific[j][0]]:
                                            user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                            break
                            elif keys[i] == "Weight":
                                height = (int(user_history["height"])**2)/100
                                if int(answer)/height > 25:
                                    for j in range(len(user_specific)):
                                        if "Fat" in disease_to_symptoms_intents[user_specific[j][0]]:
                                            user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                            break
                            elif keys[i] == "Alcohol":
                                sol = get_intents_yesNo(answer)
                                if sol == "Yes":
                                    for j in range(len(user_specific)):
                                        if "Alcohol" in disease_to_symptoms_intents[user_specific[j][0]]:
                                            user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                            break
                            elif keys[i] == "StressedLifestyle":
                                sol = get_intents_yesNo(answer)
                                if sol == "Yes":
                                    for j in range(len(user_specific)):
                                        if "StressedLifestyle" in disease_to_symptoms_intents[user_specific[j][0]]:
                                            user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                            break
                        tag=1
                        break
        elif "ChestPain" in user_intent:
            for i in range(len(keys)-1):
                if keys[i] in history_in_use:
                    if(user_history[keys[i]]==""):
                        user_history[keys[i]]=answer
                        for k in keys:
                            if(user_history[k]==""):
                                res=general_history[k]
                                break
                        if keys[i] in history_in_use:
                            if keys[i] == "Age":
                                if int(answer)>30 and int(answer)<60:
                                    for j in range(len(user_specific)):
                                        if "Middle-Age" in disease_to_symptoms_intents_chest[user_specific[j][0]]:
                                            user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                            break
                            elif keys[i] == "Weight":
                                height = (int(user_history["height"])**2)/100
                                if int(answer)/height > 25:
                                    for j in range(len(user_specific)):
                                        if "Fat" in disease_to_symptoms_intents_chest[user_specific[j][0]]:
                                            user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                            break
                            elif keys[i] == "Alcohol":
                                sol = get_intents_yesNo(answer)
                                if sol == "Yes":
                                    for j in range(len(user_specific)):
                                        if "Alcohol" in disease_to_symptoms_intents_chest[user_specific[j][0]]:
                                            user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                            break
                            elif keys[i] == "StressedLifestyle":
                                sol = get_intents_yesNo(answer)
                                if sol == "Yes":
                                    for j in range(len(user_specific)):
                                        if "StressedLifestyle" in disease_to_symptoms_intents_chest[user_specific[j][0]]:
                                            user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                            break
                        tag=1
                        break
        # print("harsh",i)
        i+=1
        if (i == len(keys)-1 and tag==0):
            if("AbdomenPain" in user_intent):
                
                user_history[keys[i]]=answer
                sol = get_intents_yesNo(answer)
                if sol == "Yes":
                    for j in range(len(user_specific)):
                        if "SimilarHistory" in disease_to_symptoms_intents[user_specific[j][0]]:
                            user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                            break
                res = "Thank You!"
            elif("ChestPain" in user_intent):
                user_history[keys[i]]=answer
                sol = get_intents_yesNo(answer)
                if sol == "Yes":
                    for j in range(len(user_specific)):
                        if "SimilarHistory" in disease_to_symptoms_intents_chest[user_specific[j][0]]:
                            user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                            break
                res = "Thank You!"
    return res

def bot_history_initial(user_history,user_specific,user_intent,answer):
    res = ""
    i=0
    if answer == "":
        for k in user_history.keys():
            if(user_history[k]==""):
                res=general_history[k]
                break
    else:
        keys=list(user_history.keys())
        tag=0
        i = 0
        if "AbdomenPain" in user_intent:
            for i in range(len(keys)-1):
                if(user_history[keys[i]]==""):
                    user_history[keys[i]]=answer
                    res=general_history[keys[i+1]]
                    if keys[i] in history_in_use:
                        if keys[i] == "Age":
                            if int(answer)>30 and int(answer)<60:
                                for j in range(len(user_specific)):
                                    if "Middle-Age" in disease_to_symptoms_intents[user_specific[j][0]]:
                                        user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                        break
                        elif keys[i] == "Weight":
                            height = (int(user_history["height"])**2)/100
                            if int(answer)/height > 25:
                                for j in range(len(user_specific)):
                                    if "Fat" in disease_to_symptoms_intents[user_specific[j][0]]:
                                        user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                        break
                        elif keys[i] == "Alcohol":
                            sol = get_intents_yesNo(answer)
                            if sol == "Yes":
                                for j in range(len(user_specific)):
                                    if "Alcohol" in disease_to_symptoms_intents[user_specific[j][0]]:
                                        user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                        break
                        elif keys[i] == "StressedLifestyle":
                            sol = get_intents_yesNo(answer)
                            if sol == "Yes":
                                for j in range(len(user_specific)):
                                    if "StressedLifestyle" in disease_to_symptoms_intents[user_specific[j][0]]:
                                        user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                        break
                    tag=1
                    break
        elif "ChestPain" in user_intent:
            for i in range(len(keys)-1):
                if(user_history[keys[i]]==""):
                    user_history[keys[i]]=answer
                    res=general_history[keys[i+1]]
                    if keys[i] in history_in_use:
                        if keys[i] == "Age":
                            if int(answer)>30 and int(answer)<60:
                                for j in range(len(user_specific)):
                                    if "Middle-Age" in disease_to_symptoms_intents_chest[user_specific[j][0]]:
                                        user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                        break
                        elif keys[i] == "Weight":
                            height = (int(user_history["height"])**2)/100
                            if int(answer)/height > 25:
                                for j in range(len(user_specific)):
                                    if "Fat" in disease_to_symptoms_intents_chest[user_specific[j][0]]:
                                        user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                        break
                        elif keys[i] == "Alcohol":
                            sol = get_intents_yesNo(answer)
                            if sol == "Yes":
                                for j in range(len(user_specific)):
                                    if "Alcohol" in disease_to_symptoms_intents_chest[user_specific[j][0]]:
                                        user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                        break
                        elif keys[i] == "StressedLifestyle":
                            sol = get_intents_yesNo(answer)
                            if sol == "Yes":
                                for j in range(len(user_specific)):
                                    if "StressedLifestyle" in disease_to_symptoms_intents_chest[user_specific[j][0]]:
                                        user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                                        break
                    tag=1
                    break
        # print("harsh",i)
        i+=1
        if (i == len(keys)-1 and tag==0):
            if("AbdomenPain" in user_intent):
                
                user_history[keys[i]]=answer
                sol = get_intents_yesNo(answer)
                if sol == "Yes":
                    for j in range(len(user_specific)):
                        if "SimilarHistory" in disease_to_symptoms_intents[user_specific[j][0]]:
                            user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                            break
                res = "Thank You!"
            elif("ChestPain" in user_intent):
                user_history[keys[i]]=answer
                sol = get_intents_yesNo(answer)
                if sol == "Yes":
                    for j in range(len(user_specific)):
                        if "SimilarHistory" in disease_to_symptoms_intents_chest[user_specific[j][0]]:
                            user_specific[j] = (user_specific[j][0],user_specific[j][1]+2)
                            break
                res = "Thank You!"
    return res