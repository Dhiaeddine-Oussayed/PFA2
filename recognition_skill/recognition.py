from os import listdir
from numpy import array
from os.path import join
from cv2 import imread, IMREAD_GRAYSCALE, resize
from random import shuffle
from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from tqdm import tqdm
from pickle import dump

all_directory = "pic_data"
img_size = (200, 200)
data = []
classes = []

for people in listdir(all_directory):
    pictures_directory = join(all_directory, people)
    for pic in tqdm(listdir(pictures_directory)):
        img_path = join(pictures_directory, pic)
        image = imread(img_path, IMREAD_GRAYSCALE)
        resized = resize(image, img_size)
        data.append([resized, people])
        if people not in classes:
            classes.append(people)
shuffle(data)

x_train = [items[0] for items in data]
y_train = [items[1] for items in data]
del data
x_train = array(x_train)/255.0
le = LabelEncoder()
encoder = le.fit(y_train)
y_train = encoder.transform(y_train)
y_train = to_categorical(y_train, len(classes))

input_shape = (200, 200, 1)

model = Sequential()
model.add(Conv2D(16, (3, 3), activation='relu', input_shape=input_shape))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(16, activation='relu'))

model.add(Dense(2, activation='softmax'))

model.summary()
model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])

history = model.fit(x_train, y_train, batch_size=32, epochs=10, validation_split=0.2)


model.save('face_recognition_model')
with open('encoder.pkl', 'wb') as f:
    dump(encoder, f)
