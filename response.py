from telegram.ext import *
import numpy as np
import pandas as pd
import pickle
from nltk.stem import PorterStemmer
from googlesearch import search

ps = PorterStemmer()
disease=""
def sample(input_text):
    message=str(input_text).lower()
    print(message)
    if message.find("symptom")!=-1 or message.find("symptoms")!=-1:
        print("Reached symptoms")
        ps = PorterStemmer()

        # loading model
        loaded_model = pickle.load(open("finalized_model.sav", 'rb'))

        # Unpickle dataframes
        symptom_severity = pd.read_pickle("symptom_severity.pkl")
        disease_description = pd.read_pickle("disease_description.pkl")
        disease_precaution = pd.read_pickle("disease_precaution.pkl")

        def DiseasePrediction(text):

            bool_list = []
            global disease
            text_token_list = text.split()
            text_token_list = [ps.stem(w) for w in text_token_list]
            text_token_set = set(text_token_list)

            for ele in symptom_severity["Symptom"]:
                ele = ele.split('_')
                ele = [ps.stem(w) for w in ele]
                ele_set = set(ele)

                flag = 0

                for i in range(len(text_token_list)):
                    if (len(ele) > 1):
                        if (ele_set.issubset(text_token_set)):
                            flag = 1
                        else:
                            flag = 0
                    else:
                        if (text_token_list[i] == ele[0]):
                            flag = 1
                        else:
                            flag = 0

                bool_list.append(flag)

            symptom_severity["bool_list"] = bool_list
            symptom_severity["weight_bool_list"] = symptom_severity["weight"] * symptom_severity["bool_list"]
            weight_bool_list = list(symptom_severity["weight_bool_list"])

            # Disease Prediction
            X_arr = np.array(weight_bool_list)
            is_all_zero = np.all((X_arr == 0))
            if is_all_zero:
                disease="Sorry, your symptoms don't match our database.\n"
                disease = disease + "These following links can help:-\n"
                for i in search(message, tld="com", num=10, stop=10, pause=1):
                    disease = disease + i + "\n"
            else:
                y_pred = loaded_model.predict(X_arr.reshape(1, -1))
                Predicted_Disease = y_pred[0]
                disease = "We are predicitng you have: " + Predicted_Disease.upper() + "\n"
                for i in range(len(disease_description)):
                    if (disease_description["Disease"][i] == Predicted_Disease):
                        disease = disease + "Description of the disease :- \n" + disease_description["Description"][i] + "\n"
                # Disease Precaution
                for i in range(len(disease_precaution)):
                    if (disease_precaution["Disease"][i] == Predicted_Disease):
                        disease = disease + "Precautions that can be taken:-\n"
                        disease = disease + "PRECAUTION 1: " + disease_precaution["Precaution_1"][i] + "\n"
                        disease = disease + "PRECAUTION 2: " + disease_precaution["Precaution_2"][i] + "\n"
                        disease = disease + "PRECAUTION 3: " + disease_precaution["Precaution_3"][i] + "\n"
                        disease = disease + "PRECAUTION 4: " + disease_precaution["Precaution_4"][i] + "\n"
                disease=disease+"To know more, you can refer to these links:-\n"
                for i in search(message, tld="com", num=10, stop=10, pause=1):
                    disease = disease + i + "\n"


        DiseasePrediction(message)
        return disease

    elif message.find('hospitals')!=-1 or message.find('hospital')!=-1:
        sen=""
        for i in search(message, tld="com", num=10, stop=10, pause=1):
            sen=sen+i+"\n"
        return (sen)
    else:
        return("Welcome onboard!\n We are Team CureTalk\n\nPlease type in the following to help us reach you\n1. /help: This gives you a complete description about our work and what we intend to do \n2. /symptoms: This helps us understand your symptoms and give you a basic layout of what needs to be done. \n3. /hospitals: We give you lists of hospitals in your area so that you can rush in immediately. \n4. /exit: To terminate our service for the moment. \n We hope this helps!")
