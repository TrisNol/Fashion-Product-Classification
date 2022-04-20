from tensorflow import keras

def train_model(train_images: list, train_labels: list, test_images: list, test_labels: list) -> keras.Model:
    """Train a conv. neural network using the provided input

    Args:
        train_images (list): JPG images as np.array used for training
        train_labels (list): Multi-label representation of labels
        test_images (list): JPG images as np.array used for testing
        test_labels (list): Multi-label representation of labels

    Returns:
        keras.Model: Trained model
    """

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

def save_model(model: keras.Model, path: str) -> None:
    """Persist the given Keras model to disk

    Args:
        model (keras.Model): Model to be saved
        path (str): Path of location
    """
    model.save(path)
    print('Saved model to disk')
