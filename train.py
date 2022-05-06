from keras.models import Sequential
import json
import numpy as np
from keras import Input
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

dataset = json.load(open('dataset.json'))

df = pd.DataFrame(dataset, columns=['text', 'label'])
df['text'] = df['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
df['text'] = df['text'].str.replace('[^\w\s]', '')
#df['text'] = df['text'].apply(lambda y: str(TextBlob(y).correct()))
#df['text'] = df['text'].apply(lambda z: " ".join([WordNetLemmatizer().lemmatize(word) for word in z.split()]))

df.sample(frac=1)
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

tfidf = vectorizer.fit(x_train_list)
A = vectorizer.transform(x_train_list)
B = vectorizer.transform(x_test_list)

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

history = model.fit(A, Y_train, validation_data=(B, Y_test), batch_size=40, epochs=20, verbose=1)

model.save("ann_model")
pickle.dump(tfidf, open("tfidf.pkl", "wb"))
