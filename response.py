import numpy as np
import pandas as pd
import pickle
from telegram.ext import *
from nltk.stem import PorterStemmer
from googlesearch import search

ps = PorterStemmer()
disease=""

def DiseasePrediction(text):
    bool_list = []
    text_token_list = text.split()
    text_token_list = [ps.stem(w) for w in text_token_list]
    text_token_set = set(text_token_list)
    for ele in symptom_severity["Symptom"]:
        ele = ele.split('_')
        ele = [ps.stem(w) for w in ele]
        ele_set = set(ele)
        flag=0
        for i in range(len(text_token_list)):
            if(len(ele) > 1):
                if(ele_set.issubset(text_token_set)):
                    flag = 1
                else:
                    flag = 0
            else:
                if(text_token_list[i] == ele[0]):
                    flag = 1
                else:
                    flag = 0
        bool_list.append(flag)
    symptom_severity["bool_list"] = bool_list
    symptom_severity["weight_bool_list"] = symptom_severity["weight"] * symptom_severity["bool_list"]
    weight_bool_list = list(symptom_severity["weight_bool_list"])
    X_arr = np.array(weight_bool_list)
    is_all_zero = np.all((X_arr == 0))
    if is_all_zero:
        result = "Sorry, your symptoms don't match our database.We think that you need to provide more symtoms.Please add more symptoms"
    else:
        y_pred = loaded_model.predict(X_arr.reshape(1, -1))
        Predicted_Disease = y_pred[0]
        result = "WE ARE PREDICTING THAT YOU HAVE ------- " + str(Predicted_Disease.upper()) + "  \n" + "  \n"
        for i in range(len(disease_description)):
            if (disease_description["Disease"][i] == Predicted_Disease):
                result = result + "DESCRIPTION OF THE DISEASE : ---- \n" + str(disease_description["Description"][i]) + "  \n" + "  \n"
                break
        for i in range(len(disease_precaution)):
            if (disease_precaution["Disease"][i] == Predicted_Disease):
                
                result = result + "PRECAUTUIONs OF THE DISEASE : ---- \n"
                result = result + "PRECAUTUION 1 : " +str(disease_precaution["Precaution_1"][i]) + "  \n" 
                result = result + "################# \n" + "  \n"
        
                result = result + "PRECAUTUION 2 : " +str(disease_precaution["Precaution_2"][i]) + "  \n" 
                result = result + "################# \n" + "  \n"
                
                result = result + "PRECAUTUION 3 : " +str(disease_precaution["Precaution_3"][i]) + "  \n" 
                result = result + "################# \n" + "  \n"
                
                result = result + "PRECAUTUION 4 : " +str(disease_precaution["Precaution_4"][i])+ "  \n" 
                result = result + "################# \n" + "  \n"
                break
    return result
def sample(input_text):
    message=str(input_text).lower()
    print(message)
    if message.find("symptom")!=-1 or message.find("symptoms")!=-1:
        print("Reached symptoms")
        loaded_model = pickle.load(open("finalized_model.sav", 'rb'))
        symptom_severity = pd.read_pickle("symptom_severity.pkl")
        disease_description = pd.read_pickle("disease_description.pkl")
        disease_precaution = pd.read_pickle("disease_precaution.pkl")
        disease = DiseasePrediction(message)
        return disease
    elif message.find('hospitals')!=-1 or message.find('hospital')!=-1:
        sen=""
        print("Reached hospitals")
        for i in search(message, tld="com", num=10, stop=10, pause=1):
            sen=sen+i+"\n"
        return sen
    else:
        return("Welcome onboard!\n We are Team CureTalk\n\nPlease type in the following to help us reach you\n1. /help: This gives you a complete description about our work and what we intend to do \n2. /symptoms: This helps us understand your symptoms and give you a basic layout of what needs to be done. \n3. /hospitals: We give you lists of hospitals in your area so that you can rush in immediately. \n4. /exit: To terminate our service for the moment. \n We hope this helps!")

ps = PorterStemmer()

# loading model
loaded_model = pickle.load(open("finalized_model.sav", 'rb'))

#Unpickle dataframes
symptom_severity = pd.read_pickle("symptom_severity.pkl")
disease_description = pd.read_pickle("disease_description.pkl")
disease_precaution = pd.read_pickle("disease_precaution.pkl")

    

symptoms_by_user = input("Write about your SYMPTOMS: ")
predicted_result = DiseasePrediction(symptoms_by_user)
print(predicted_result)