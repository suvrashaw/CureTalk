from telegram.ext import *
import response as r

API_KEY="1977152020:AAGfZUZ9fHqadNDji8WjiPr466dNJo1vfLk"

def help(update,context):
    update.message.reply_text("Hello! This is Team Cure Talk.")
    update.message.reply_text("\nWe are 5 students from UEMK who have come up with a plan to put Computer Science to mankind's best use!")
    update.message.reply_text("Our team involves:- \n1. Mehuly Chakraborthy \n2. Suvra Shaw \n3. Diptaraj Sen \n4. Saranya Bhattacharjee\n5. Kaustav Roy")
    update.message.reply_text(" We aim to bring to you the basic medical need that might help cure you.")
    update.message.reply_text("From hospitals to treatments, our bot can work miracles in dire needs")
    update.message.reply_text("\n We hope to own a small part in your recovery journey! Thank you!")

def exit(update,context):
    update.message.reply_text("Thank you for being with us! Team CureTalk wishes you the best of health.")

def symptoms(update,context):
    update.message.reply_text("Please type in your symptoms.")
    update.message.reply_text("PLEASE START THE SENTENCE WITH THE WORD: Symptom is/Symptoms are")

def hospitals(update,context):
    update.message.reply_text("Please enter the city that you live in, in the following manner.")
    update.message.reply_text("Hospitals in {your city name}.\nFor eg: Hospitals in Chennai")

def handle_message(update,context):
    text = str(update.message.text).lower()
    response=r.sample(text)
    update.message.reply_text(response)

def error(update,context):
    print("Error")

def main():
    updater=Updater(API_KEY,use_context=True)
    dp= updater.dispatcher
    dp.add_handler(CommandHandler("help",help))
    dp.add_handler(CommandHandler("exit", exit))
    dp.add_handler(CommandHandler("symptoms", symptoms))
    dp.add_handler(CommandHandler("hospitals", hospitals))
    dp.add_error_handler(error)
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    updater.start_polling()
    updater.idle()

main()