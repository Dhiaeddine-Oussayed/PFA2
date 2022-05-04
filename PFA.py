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
from pandas import Index
from googletrans import Translator
from time import sleep
from itertools import chain
from pygame import mixer


environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tfidf = load(open("tfidf.pkl", "rb"))
model = models.load_model("ann_model")
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


def oos():
    return choice(list_library.oos)


def user_name():
    global User_name
    if User_name == '':
        text = choice(list_library.no_name)
        print('Assistance: ', text)
        engine.say(text)
        engine.runAndWait()
        wish = listen()
        tagged = pos_tag(word_tokenize(wish))
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


def listen():
    # with Microphone() as source:
    #     print("User:", end=' ')
    #     voice = Recognizer().listen(source)
    # return Recognizer().recognize_google(voice)
    print("User:", end=' ')
    return input()


def prediction(intention):
    test = [intention]
    test = tfidf.transform(test)
    test.sort_indices()
    predicted = model.predict(test)
    return argmax(predicted)


def talk(speech):
    print('Assistance: ', speech)
    engine.say(speech)
    engine.runAndWait()


def playAlarm():
    mixer.init()
    mixer.music.load(r'Alarm.mp3')
    mixer.music.play()


def timer(com):
    a = list(chain(*pos_tag(word_tokenize(com))))
    time_dic = {"hours": 0, "minutes": 0, "seconds": 0}
    talk('Your timer has started')
    for i in range(len(a)):
        if a[i] == 'second' or a[i] == 'seconds':
            time_dic['seconds'] = int(a[i - 2])
        elif a[i] == 'minutes' or a[i] == 'minute':
            time_dic['minutes'] = int(a[i - 2])
        elif a[i] == 'hours' or a[i] == 'hour':
            time_dic['hours'] = int(a[i - 2])
    timer_time = time_dic["hours"]*3600 + time_dic["minutes"]*60 + time_dic["seconds"]
    sleep(timer_time-8.349)
    talk('Your timer finishes in 5 seconds')
    for i in range(5):
        sleep(1)
        print("Timer finished in ", 5 - i)
    playAlarm()
    return


def translate(com):
    talk('Sure ! What do you want to translate?')
    query = listen()
    phrase = word_tokenize(com)
    if 'in' in phrase:
        dest = phrase[phrase.index('in')+1]
    else:
        talk('To which language?')
        dest = listen()
    translator = Translator()
    talk(" ".join(["Your result for translating *", query, "* in", dest, 'is']))
    change_voice(engine, 'fr_CA', "VoiceGenderFemale")
    talk(translator.translate(query, dest=dest[:2]).text)
    change_voice(engine, 'en_US', "VoiceGenderFemale")

def change_voice(eng, language, gender='VoiceGenderFemale'):
    for voice in eng.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            eng.setProperty('voice', voice.id)
            return True


engine = init()
change_voice(engine, 'en_US', "VoiceGenderFemale")
classes = Index(['label_calculator', 'label_courtesygreeting', 'label_definition',
                 'label_goodbye', 'label_greeting', 'label_namequery', 'label_next_song',
                 'label_notebook', 'label_oos', 'label_play_music', 'label_screenshot',
                 'label_tell_joke', 'label_thank_you', 'label_time', 'label_timer',
                 'label_translate', 'label_user_name', 'label_volumedown',
                 'label_volumeup', 'label_weather', 'label_what_can_i_ask_you'],
                dtype='object')


def main():
    while 1:
        answer = ''
        command = listen()
        print(command)
        predicted_class = prediction(command)
        print(classes[predicted_class])
        if classes[predicted_class] == 'label_greeting':
            answer = greeting()
        elif classes[predicted_class] == 'label_courtesygreeting':
            answer = courtesey_greeting()
        elif classes[predicted_class] == 'label_thank_you':
            answer = thanks()
        elif classes[predicted_class] == 'label_tell_joke':
            answer = jokes()
        elif classes[predicted_class] == 'label_namequery':
            answer = bot_name()
        elif classes[predicted_class] == 'label_time':
            answer = time()
        elif classes[predicted_class] == 'label_user_name':
            answer = user_name()
        elif classes[predicted_class] == 'label_what_can_i_ask_you':
            skills()
        elif classes[predicted_class] == 'label_volumedown':
            volume_down()
        elif classes[predicted_class] == 'label_volumeup':
            volume_up()
        elif classes[predicted_class] == 'label_screenshot':
            Screenshot()
        elif classes[predicted_class] == 'label_oos':
            answer = oos()
        elif classes[predicted_class] == 'label_translate':
            translate(command)
        elif classes[predicted_class] == 'label_timer':
            timer(command)
        elif classes[predicted_class] == 'label_goodbye':
            answer = goodbye()
            print('Assistance: ', answer)
            engine.say(answer)
            engine.runAndWait()
            break
        if answer == '':
            answer = 'Anything else?'
        talk(answer)


if __name__ == '__main__':
    main()

# def alarm():
# def TakePicture():
# def calculator()
# def calendar()
# def definition()
# def music()
# def Meeting()
# def spelling()
# def timer()
# def weather()
# def info()
# def mail()
# def notebook()
# def stop()
