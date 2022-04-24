from numpy import argmax
import random
from datetime import datetime
import pyautogui
import list_library
from keras.models import Sequential
from keras import Input
from keras.layers import Dense
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import speech_recognition as sr
import pickle



dataset = json.load(open('dataset.json'))

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

# vectorizer = TfidfVectorizer()
tfidf = pickle.load(open("tfidf.pkl", "rb"))
A = tfidf.transform(x_train_list)
B = tfidf.transform(x_test_list)

A.sort_indices()
B.sort_indices()
number_of_classes = len(set(Y))

model = Sequential()
model.add(Input(shape=A.shape[1]))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))

model.add(Dense(number_of_classes, activation='softmax'))

model.compile(optimizer="Adam", loss="categorical_crossentropy", metrics=["accuracy"])

print(model.summary())

history = model.fit(A, Y_train, validation_data=(B, Y_test), batch_size=30, epochs=10, verbose=1)


# pickle.dump(tfidf, open("tfidf.pkl", "wb"))


recording = sr.Recognizer()
with sr.Microphone() as source:
    print("Please Say something:")
    voice = recording.listen(source)
    command = recording.recognize_google(voice)

print(command)

test = [command]
test = tfidf.transform(test)
test.sort_indices()
prediction = model.predict(test)
predicted_class = argmax(prediction)
print(Y.columns[predicted_class])

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
