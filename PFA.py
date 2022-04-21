from numpy import argmax
import random
from datetime import datetime
import pyautogui
import list_library
import speech_recognition as sr
from keras.models import load_model
import prepare_data

model = load_model('data')


recording = sr.Recognizer()
with sr.Microphone() as source:
    print("Please Say something:")
    voice = recording.listen(source)
    command = recording.recognize_google(voice)

print(command)

test = [command]
test = prepare_data.vectorizer.transform(test)
test.sort_indices()
prediction = model.predict(test)
predicted_class = argmax(prediction)
print(prepare_data.Y.columns[predicted_class])

UserNameAsked = False


def greeting():
    text = list_library.greetings
    return random.choice(text)


def goodbye():
    text = list_library.goodbyes
    return random.choice(text)


def thanks():
    text = list_library.thanks
    return random.choice(text)


def bot_name():
    text = list_library.bot_name
    return random.choice(text)


def time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def jokes():
    joke = list_library.jokes
    return random.choice(joke)


def user_name():
    global UserNameAsked
    if not UserNameAsked:
        text = list_library.no_name

    else:
        text = ["You are {}! How can I help?",
                "Your name is  {}, how can I help you?",
                "They call you {}, what can I do for you?",
                "Your name is {}, how can I help you?",
                "{}, what can I do for you?"
                ]
    return random.choice(text)


def do_you_understand():
    text = list_library.understand
    return random.choice(text)


def shutup():
    text = list_library.shutup
    return random.choice(text)


def volume_up():
    for vu in range(5):
        pyautogui.press('volumeup')


def volume_down():
    for vd in range(5):
        pyautogui.press('volumedown')


def screenshot():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'D:\DHIA\PyCharm Community Edition 2021.2.1\screenshots')

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
