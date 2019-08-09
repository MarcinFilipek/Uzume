import os
from PIL import Image
import numpy as np
import cv2

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten, Conv2D
from tensorflow.python.keras.layers import MaxPool2D, Dropout
from tensorflow.python.keras.models import model_from_json

data_path = 'Persons/Persons_data'
train_data_path = os.path.join(data_path, 'Train')
test_data_path = os.path.join(data_path, 'Val')

train_filipek_path = os.path.join(train_data_path, 'Filipek')
train_others_path = os.path.join(train_data_path, 'Others')

test_filipek_path = os.path.join(test_data_path, 'Filipek')
test_others_path = os.path.join(test_data_path, 'Others')

X_train = []
y_train = []

X_test = []
y_test = []


for i, j in zip(os.listdir(train_filipek_path), os.listdir(train_others_path)):
    image = Image.open(os.path.join(train_filipek_path, i))
    data = np.asarray(image)
    data = cv2.resize(data, (200, 200))
    X_train.append(data)
    y_train.append(1)
    image = Image.open(os.path.join(train_others_path, j))
    data = np.asarray(image)
    data = cv2.resize(data, (200, 200))
    X_train.append(data)
    y_train.append(0)

for i, j in zip(os.listdir(test_filipek_path), os.listdir(test_others_path)):
    image = Image.open(os.path.join(test_others_path, j))
    data = np.asarray(image)
    data = cv2.resize(data, (200, 200))
    X_test.append(data)
    y_test.append(0)
    image = Image.open(os.path.join(test_filipek_path, i))
    data = np.asarray(image)
    data = cv2.resize(data, (200, 200))
    X_test.append(data)
    y_test.append(1)


X_train = np.asarray(X_train)
y_train = np.asarray(y_train)

X_test = np.asarray(X_test)
y_test = np.asarray(y_test)


X_train = np.reshape(X_train, newshape=(-1, 200, 200, 1))
X_train = X_train / 255

X_test = np.reshape(X_test, newshape=(-1, 200, 200, 1))
X_test = X_test / 255

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)

# Load or training model
loadmodel = input('Load model [y/n]?')
if loadmodel == 'y':
    with open('model_architecture.json', 'r') as f:
        model = model_from_json(f.read())
    model.load_weights('model_weights.h5')
else:
    input_shape = (200, 200, 1)
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), input_shape=input_shape, activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))


model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

if loadmodel == 'n':
    model.fit(X_train, y_train, batch_size=20, epochs=15, validation_split=0.2)

# Test model
model.evaluate(X_test, y_test)

save_model = input('Save model [y/n]?')
if save_model == 'y':
    model.save_weights('model_weights.h5')
    with open('model_architecture.json', 'w') as f:
        f.write(model.to_json())


image = Image.open('Persons/Persons_data/Val/Filipek/Filipek_5.jpg')
data = np.asarray(image)
data = cv2.resize(data, (200, 200))
data = np.reshape(data, newshape=(-1, 200, 200, 1))
data = data / 255
print(model.predict(data))