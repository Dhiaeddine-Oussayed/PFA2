import os
from numpy import argmax
from nltk import word_tokenize, pos_tag
from random import choice
from datetime import datetime, date
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

bot_name = 'Assistance'

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


def Bot_name():
    Bot_name_list = [f"You can call me {bot_name}", f"You may call me {bot_name}",
                     f"Call me {bot_name}", f"I am your intelligent bot, {bot_name}"]
    return choice(Bot_name_list)


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
        for i, j in tagged:
            if j == 'NNP':
                User_name = i
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
    print(bot_name, ': ', speech)
    engine.say(speech)
    engine.runAndWait()


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


def change_ai_name():
    global bot_name
    talk("To what name?")
    bot_name = listen()
    talk("I got that, from now on my name will be " + bot_name)

def change_user_name():
    global User_name
    talk("To what name?")
    User_name = listen()

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
    print(destination)
    translator = Translator()
    talk(" ".join(["Your result for translating *", query, "* in", dest, 'is']))
    change_voice(engine, destination, "VoiceGenderMale")
    talk(translator.translate(query, dest=destination[:2]).text)
    change_voice(engine, 'en_US', "VoiceGenderFemale")


def change_voice(eng, language, gender='VoiceGenderFemale'):
    for voice in eng.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            eng.setProperty('voice', voice.id)
            return True


engine = init()
change_voice(engine, 'en_US', "VoiceGenderFemale")
classes = load(open("Labels.pkl", "rb"))


def main():
    global stop_threads, index, User_name
    talk('Welcome, I am ' + bot_name + ' your favourite virtual assistant')
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
                index = len(playlist) - 1
            stop_threads = True
            _exit.set()
        else:
            predicted_class_INDEX = prediction(command)
            # print(predicted_class)
            predicted_class = classes[predicted_class_INDEX]
            if predicted_class == 'label_greeting':
                answer = greeting()
            elif predicted_class == 'label_courtesygreeting':
                answer = courtesey_greeting()
            elif predicted_class == 'label_change_ai_name':
                change_ai_name()
            elif predicted_class == 'label_play_music':
                music_thread = Thread(target=play_music)
                music_thread.start()
            elif predicted_class == 'label_next_song':
                index += 1
                if index >= len(playlist):
                    index = 0
                music_thread = Thread(target=play_music)
                music_thread.start()
            elif predicted_class == 'label_thank_you':
                answer = thanks()
            elif predicted_class == 'label_how_old_are_you':
                answer = choice(list_library.old)
            elif predicted_class == 'label_tell_joke':
                answer = jokes()
            elif predicted_class == 'label_are_you_a_bot':
                answer = choice(list_library.are_you_a_bot)
            elif predicted_class == 'label_where_are_you_from':
                answer = choice(list_library.where_are_you_from)
            elif predicted_class == 'label_namequery':
                answer = Bot_name()
            elif predicted_class == 'label_date':
                answer = str(date.today())
            elif predicted_class == 'label_who_do_you_work_for':
                answer = choice(list_library.who_do_you_work_for)
            elif predicted_class == 'label_who_made_you':
                answer = choice(list_library.who_made_you)
            elif predicted_class == 'label_do_you_have_pets':
                answer = choice(list_library.do_you_have_pets)
            elif predicted_class == 'label_change_user_name':
                change_user_name()
            elif predicted_class == 'label_what_are_your_hobbies':
                answer = choice(list_library.what_are_your_hobbies)
            elif predicted_class == 'label_time':
                answer = time()
            elif predicted_class == 'label_user_name':
                talk("Do you want me to use the camera to identify you?")
                wish = listen()
                if 'yes' in wish.lower():
                    from recognition_skill.f_classification import name
                    User_name = name[0]
                    talk('You are ' + User_name)
                    # exec(open("recognition_skill/f_classification.py").read())
                else:
                    answer = user_name()
            elif predicted_class == 'label_what_can_i_ask_you':
                skills()
            elif predicted_class == 'label_volumedown':
                volume_down()
            elif predicted_class == 'label_volumeup':
                volume_up()
            elif predicted_class == 'label_screenshot':
                Screenshot()
            elif predicted_class == 'label_oos':
                answer = oos()
            elif predicted_class == 'label_translate':
                translate(command)
            elif predicted_class == 'label_timer':
                timer_thread = Thread(target=timer, args=[timerTime(command)])
                timer_thread.start()
            elif predicted_class == 'label_say_something':
                answer = choice(list_library.say_hello)
            elif predicted_class == 'label_goodbye':
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
# def definition(to_define):


# def Meeting()
# def spelling()
# def weather()
# def info()
# def mail()
# def notebook()
# def stop()
