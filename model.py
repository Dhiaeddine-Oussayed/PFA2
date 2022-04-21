from keras.models import Sequential
from keras import Input
from keras.layers import Dense
import prepare_data

A = prepare_data.A
number_of_classes = prepare_data.number_of_classes
B = prepare_data.B
Y_train = prepare_data.Y_train
Y_test = prepare_data.Y_test

model = Sequential()
model.add(Input(shape=A.shape[1]))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))

model.add(Dense(number_of_classes, activation='softmax'))

model.compile(optimizer="Adam", loss="categorical_crossentropy", metrics=["accuracy"])

print(model.summary())

history = model.fit(A, Y_train, validation_data=(B, Y_test), batch_size=30, epochs=10, verbose=1)

model.save('data')
