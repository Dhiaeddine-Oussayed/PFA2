from numpy import argmax
from nltk import word_tokenize, pos_tag
from random import choice
from datetime import datetime
from pyautogui import press, screenshot
import list_library
from keras import models
from speech_recognition import Recognizer, Microphone
from pickle import load
from os import environ
from pyttsx3 import init
from train import Y
tfidf = load(open("tfidf.pkl", "rb"))
model = models.load_model("ann_model")


environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

User_name = ''
def greeting():
    text = list_library.greetings
    return choice(text)
def courtesey_greeting():
    text = list_library.courtesey_greeting
    return choice(text)
def goodbye():
    text = list_library.goodbyes
    return choice(text)
def thanks():
    text = list_library.thanks
    return choice(text)
def bot_name():
    text = list_library.bot_name
    return choice(text)
def time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time
def jokes():
    joke = list_library.jokes
    return choice(joke)
def user_name():
    global User_name
    if User_name == '':
        text = choice(list_library.no_name)
        print('Assistance: ', text)
        engine.say(text)
        engine.runAndWait()
        with Microphone() as mic:
            print("User:")
            sound = recording.listen(mic)
            wish = recording.recognize_google(sound)
        words = word_tokenize(wish)
        tagged = pos_tag(words)
        for i in tagged:
            if i[1] == 'NNP':
                User_name = i[0]
                break
        return "I'll put that in mind"
    else:
        text = [f"You are {User_name}! How can I help?",
                f"Your name is  {User_name}, how can I help you?",
                f"They call you {User_name}, what can I do for you?",
                f"Your name is {User_name}, how can I help you?",
                f"{User_name}, what can I do for you?"
                ]
        return choice(text)
def skills():
    engine.say('This is a list of what I can do: ')
    engine.runAndWait()
    print(list_library.skills)
def do_you_understand():
    text = list_library.understand
    return choice(text)
def volume_up():
    for vu in range(5):
        press('volumeup')
def volume_down():
    for vd in range(5):
        press('volumedown')
def Screenshot():
    myScreenshot = screenshot()
    myScreenshot.save(r'D:\DHIA\PyCharm Community Edition 2021.2.1\screenshots')
    print('Screenshot saved successfully!')


def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True
engine = init()
change_voice(engine, 'en_US', "VoiceGenderFemale")

print(set(Y.columns))

recording = Recognizer()
while True:
    answer = ''
    with Microphone() as source:
        print("User:")
        voice = recording.listen(source)
        command = recording.recognize_google(voice)
    print(command)
    test = [command]
    test = tfidf.transform(test)
    test.sort_indices()
    prediction = model.predict(test)
    predicted_class = argmax(prediction)
    if Y.columns[predicted_class] == 'label_greeting':
        answer = greeting()
    elif Y.columns[predicted_class] == 'label_courtesygreeting':
        answer = courtesey_greeting()
    elif Y.columns[predicted_class] == 'label_thank_you':
        answer = thanks()
    elif Y.columns[predicted_class] == 'label_tell_joke':
        answer = jokes()
    elif Y.columns[predicted_class] == 'label_goodbye':
        answer = goodbye()
        print('Assistance: ', answer)
        engine.say(answer)
        engine.runAndWait()
        break
    elif Y.columns[predicted_class] == 'label_namequery':
        answer = bot_name()
    elif Y.columns[predicted_class] == 'label_time':
        answer = time()
    elif Y.columns[predicted_class] == 'label_user_name':
        answer = user_name()
    elif Y.columns[predicted_class] == 'label_what_can_i_ask_you':
        skills()
    elif Y.columns[predicted_class] == 'label_volumedown':
        volume_down()
    elif Y.columns[predicted_class] == 'label_volumeup':
        volume_up()
    elif Y.columns[predicted_class] == 'label_screenshot':
        Screenshot()
    if answer == '':
        answer = 'Anything else?'
    print('Assistance: ', answer)
    engine.say(answer)
    engine.runAndWait()

# def alarm():
# def TakePicture():
# def repeat()
# def calculator()
# def calendar()
# def definition()
# def music()
# def Meeting()
# def spelling()
# def timer()
# def translate()
# def weather()
# def info()
# def mail()
# def notebook()
# def stop()
# def oos()
