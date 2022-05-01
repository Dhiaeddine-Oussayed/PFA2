import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import speech_recognition as sr

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

vectorizer = TfidfVectorizer()
A = vectorizer.fit_transform(x_train_list)
B = vectorizer.transform(x_test_list)

A.sort_indices()
B.sort_indices()

number_of_classes = len(set(Y))
labels = []
for i in dataset:
    labels.append(i[1])

print(number_of_classes)
print(len(dataset))
print(len(set(labels)))
print(A.shape)
print(B.shape)

recording = sr.Recognizer()
with sr.Microphone() as source:
    print("Please Say something:")
    voice = recording.listen(source)
    command = recording.recognize_google(voice)

print(command)
test = [command]
test = vectorizer.transform(test)
test.sort_indices()

print(test.shape)



