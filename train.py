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

print("Loading dataset...")
dataset = json.load(open('dataset.json'))
print("Dataset loaded!")

print("Converting to dataframe...")
df = pd.DataFrame(dataset, columns=['text', 'label'])
print("Converted!")
print("Lowering...")
df['text'] = df['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
print("Done!")
print("Removing punctuation...")
df['text'] = df['text'].str.replace('[^\w\s]', '')
print("Punctuation removed!")
print("Correcting grammatical mistakes...")
df['text'] = df['text'].apply(lambda y: str(TextBlob(y).correct()))
print("Mistakes corrected!")
print("Lemmatizing...")
df['text'] = df['text'].apply(lambda z: " ".join([WordNetLemmatizer().lemmatize(word) for word in z.split()]))
print("Dataframe lemmatized!")

print("Preprocessing started...")
df.sample(frac=1)
dummies = ['label']
dataframe = pd.get_dummies(df, columns=dummies)

X = dataframe["text"]
Y = dataframe.drop(['text'], axis=1)

labels = Y.columns

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

print("Preprocessing done!")

model = Sequential()
model.add(Input(shape=A.shape[1]))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))

model.add(Dense(number_of_classes, activation='softmax'))

model.compile(optimizer="Adam", loss="categorical_crossentropy", metrics=["accuracy"])

print(model.summary())

print("Training Started...")
history = model.fit(A, Y_train, validation_data=(B, Y_test), batch_size=40, epochs=20, verbose=1)
print("Training done!")

print("Saving the model...")
model.save("ann_model")
print("Model saved!")
print("saving tfidf...")
pickle.dump(tfidf, open("tfidf.pkl", "wb"))
print("tfidf saved!")
print("Saving Labels...")
pickle.dump(labels, open("Labels.pkl", "wb"))
print("Labels saved!")
