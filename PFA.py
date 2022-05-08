import os
from numpy import argmax
from nltk import word_tokenize, pos_tag
from random import choice
from datetime import datetime
from pyautogui import press, screenshot
import list_library
from keras.models import load_model
from speech_recognition import Recognizer, Microphone
from pickle import load
from os import environ
from pyttsx3 import init
from pandas import Index
from googletrans import Translator
from time import sleep
from itertools import chain
from pygame import mixer
from threading import Thread, Event
import json
import audioread


languages = json.load(open('languages.json'))

environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tfidf = load(open("tfidf.pkl", "rb"))
model = load_model("ann_model")

User_name = ''

state = 0

_exit = Event()
mixer.init()
path = '/Users/dhiaoussayed/Music/Music/Media.localized/Music/Unknown Artist/Unknown Album'
playlist = [os.path.join(path, music) for music in os.listdir(path)]
index = 0
stop_threads = False

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
        talk(text)
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
    talk('This is a list of what I can do: ')
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
    #     command = Recognizer().recognize_google(voice)
    #     print(command)
    # return command
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
    # engine.say(speech)
    # engine.runAndWait()
def play_music():
    global index, stop_threads
    while 1:
        mixer.music.load(playlist[index])
        mixer.music.play()
        with audioread.audio_open(playlist[index]) as f:
            length = f.duration
        _exit.wait(length)
        index += 1
        if index >= len(playlist):
            index = 0
        if stop_threads:
            break
def playAlarm():
    mixer.init()
    mixer.music.load(r'Alarm.mp3')
    mixer.music.play()
def timerTime(com):
    if not any(value.isdigit() for value in com.split()):
        talk('How long would you like the timer to be?')
        com = listen()
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
    return time_dic["hours"] * 3600 + time_dic["minutes"] * 60 + time_dic["seconds"]
def timer(time_for_timer):
    global state
    state = time_for_timer
    for i in range(time_for_timer):
        sleep(1)
        state -= 1
    playAlarm()
def translate(com):
    talk('Sure ! What do you want to translate?')
    query = listen()
    phrase = word_tokenize(com)
    if 'in' in phrase:
        dest = phrase[phrase.index('in') + 1].lower()
    else:
        talk('To which language?')
        dest = listen().lower()
    destination = languages[dest]
    translator = Translator()
    talk(" ".join(["Your result for translating *", query, "* in", dest, 'is']))
    change_voice(engine, destination, "VoiceGenderFemale")
    talk(translator.translate(query, dest=destination[:2]).text)
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
                 'label_notebook', 'label_oos', 'label_play_music',
                 'label_say_something', 'label_screenshot', 'label_tell_joke',
                 'label_thank_you', 'label_time', 'label_timer', 'label_translate',
                 'label_user_name', 'label_volumedown', 'label_volumeup',
                 'label_weather', 'label_what_can_i_ask_you'],
                dtype='object')


def main():
    global stop_threads, index
    talk('Welcome, I am Assistant your favourite virtual assistant')
    while 1:
        answer = ''
        command = listen()
        if "pause the music" in command:
            mixer.music.pause()
        elif "resume the music" in command:
            mixer.music.unpause()
        elif "stop the music" in command:
            mixer.music.stop()
            index -= 1
            if index < 0:
                index = len(playlist)-1
            stop_threads = True
            _exit.set()
        else:
            predicted_class = prediction(command)
            print(classes[predicted_class])
            if classes[predicted_class] == 'label_greeting':
                answer = greeting()
            elif classes[predicted_class] == 'label_courtesygreeting':
                answer = courtesey_greeting()
            elif classes[predicted_class] == 'label_play_music':
                music_thread = Thread(target=play_music)
                music_thread.start()
            elif classes[predicted_class] == 'label_next_song':
                index += 1
                if index >= len(playlist):
                    index = 0
                music_thread = Thread(target=play_music)
                music_thread.start()
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
                timer_thread = Thread(target=timer, args=[timerTime(command)])
                timer_thread.start()
            elif classes[predicted_class] == 'label_say_something':
                answer = choice(list_library.say_hello)
            elif classes[predicted_class] == 'label_goodbye':
                answer = goodbye()
                talk(answer)
                break
            if answer == '':
                answer = 'Anything else?'
            talk(answer)


if __name__ == '__main__':
    main()

# def alarm():
# def TakePicture():
# def calculator()
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
