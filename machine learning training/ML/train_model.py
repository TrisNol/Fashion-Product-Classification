import tensorflow as tf
from tensorflow import keras
import numpy as np

def train_model(train_images, train_labels, test_images, test_labels):

    model = keras.Sequential([
        keras.layers.Conv2D(64, (3, 3), activation="relu", input_shape=(60, 80, 3)),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Flatten(),
        keras.layers.Dense(512, activation='relu'),
        # use sigmoid-function to output an array of values between 0 and 1 --> probability
        keras.layers.Dense(len(train_labels[0]), activation="sigmoid")
    ])

    model.compile(optimizer='adam', loss="binary_crossentropy",
                metrics=['accuracy'])

    model.fit(train_images, train_labels, epochs=10)

    test_loss, test_acc = model.evaluate(test_images, test_labels)
    print('\nTest accuracy: ', test_acc)
    print('\nTest loss: ', test_loss)

    return model

def save_model(model, path):
    model.save(path)
    print('Saved model to disk')
