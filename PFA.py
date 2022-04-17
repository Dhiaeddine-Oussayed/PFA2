import pandas as pd
# import nltk
import os
# import re
import json
import numpy as np
import random
from datetime import datetime
# from textblob import TextBlob
# from textblob import Word
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.models import Sequential
from keras import Input
from keras.layers import Dense
import pyautogui
import Jokes_library

# nltk.download()

DATA_DIRECTORY = 'data'
files = []
ALL_DATA = []

for file in os.listdir(DATA_DIRECTORY):
    f = open(os.path.join(DATA_DIRECTORY, file))
    ALL_DATA.append(json.load(f))
    f.close()

targets = ['volumeDown', 'volumeUp']
data_from_0 = []

for i in targets:
    for j in ALL_DATA[0]['sentences']:
        if j['intent'] == i:
            data_from_0.append([j['text'], i])

intent = ['Greeting', 'CourtesyGreeting', 'NameQuery', 'UnderstandQuery',
          'Shutup', 'CourtesyGoodBye', 'WhoAmI', 'SelfAware', 'GoodBye']
data_from_1 = []
for i in ALL_DATA[1]['intents']:
    if i['intent'] in intent:
        for j in i['text']:
            data_from_1.append([j, i['intent']])

intentions = ['meeting_schedule', 'next_song', 'play_music', 'reminder', 'repeat',
              'spelling', 'tell_joke', 'thank_you', 'time', 'timer', 'alarm', 'calculator', 'calendar',
              'date', 'definition', 'translate', 'user_name', 'weather', 'what_can_i_ask_you']
data_from_2 = []
for i in intentions:
    for j in ALL_DATA[2]:
        if j[1] == i:
            data_from_0.append([j[0], i])

dataset = data_from_0 + data_from_1 + data_from_2
df = pd.DataFrame(dataset, columns=['text', 'label'])

df['text'] = df['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
df['text'] = df['text'].str.replace('[^\w\s]', '')
# df['text'] = df['text'].apply(lambda y: str(TextBlob(y).correct()))
# df['text'] = df['text'].apply(lambda z: " ".join([Word(word).lemmatize() for word in z.split()]))

dummies = ['label']
dataframe = pd.get_dummies(df, columns=dummies)

X = dataframe["text"]
Y = dataframe.drop(['text'], axis=1)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.05)

x_train_list = x_train.tolist()
x_test_list = x_test.tolist()
Y_train = np.array(y_train)
Y_test = np.array(y_test)

vectorizer = TfidfVectorizer()
A = vectorizer.fit_transform(x_train_list)
B = vectorizer.transform(x_test_list)

A.sort_indices()
B.sort_indices()

number_of_classes = len(set(Y))

# size = A.shape[1]
# Input = Input(shape=(size,))
# Hidden_layer1 = Dense(units=128, activation='relu')(Input)
# Hidden_layer2 = Dense(units=64, activation='relu')(Hidden_layer1)
# Output_layer = Dense(number_of_classes, activation='softmax')(Hidden_layer2)
# mod = Model(Input, Output_layer)

model = Sequential()
model.add(Input(shape=A.shape[1]))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(number_of_classes, activation='softmax'))


model.compile(optimizer="Adam", loss="categorical_crossentropy", metrics=["accuracy"])


print(model.summary())

history = model.fit(A, Y_train, validation_data=(B, Y_test), batch_size=30, epochs=10, verbose=1)

test = ["can you play some music please"]
test = vectorizer.transform(test)
test.sort_indices()
prediction = model.predict(test)
predicted_class = np.argmax(prediction)
print(Y.columns[predicted_class])

UserNameAsked = False


def greeting():
    text = ["Hello, thanks for visiting", "Good to see you again", "Hi there, how can I help?", "Hey human!",
            "Good day Sir", "Hola human!"]
    return random.choice(text)


def goodbye():
    text = ["See you later, thanks for visiting", "Have a nice day", "Bye! Come back again soon.",
            "Goodbye thanks for coming"]
    return random.choice(text)


def thanks():
    text = ["No problem!", "Happy to help!", "Any time!", "My pleasure"]
    return random.choice(text)


def bot_name():
    text = ["You can call me Assistance", "You may call me Assistance", "Call me Assistance"]
    return random.choice(text)


def time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def jokes():
    joke = Jokes_library.jokes
    return random.choice(joke)


def self_aware():
    text = [
        "That is an interesting question, can you prove that you are?",
        "That is an difficult question, can you prove that you are?",
        "That depends, can you prove that you are?"
    ]
    return random.choice(text)


def user_name():
    global UserNameAsked
    if not UserNameAsked:
        text = ["You still didn't tell me your name Sir", "You didn't tell me that yet",
                "How about you tell me your name first then i'll answer that", "I'll call you Sir or Miss for now"]

    else:
        text = ["You are {}! How can I help?",
                "Your name is  {}, how can I help you?",
                "They call you {}, what can I do for you?",
                "Your name is {}, how can I help you?",
                "{}, what can I do for you?"
                ]
    return random.choice(text)


def do_you_understand():
    text = [
        "Well I would not be a very clever AI if I did not would I?",
        "I read you loud and clear!",
        "I do in deed!",
        "Yup I do"
    ]
    return random.choice(text)


def shutup():
    text = [
        "I am sorry to disturb you",
        "Fine, sorry to disturb you",
        "OK, sorry to disturb you",
        "You could just say goodbye, you don't have to be rude"
        "Rude, bye"
    ]
    return random.choice(text)


def volume_up():
    for vu in range(5):
        pyautogui.press('volumeup')


def volume_down():
    for vd in range(5):
        pyautogui.press('volumedown')


# def alarm():
# def TakePicture():

def screenshot():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(r'D:\DHIA\PyCharm Community Edition 2021.2.1\screenshots')
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
