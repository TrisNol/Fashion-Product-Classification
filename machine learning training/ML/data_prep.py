import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import tensorflow as tf
import numpy as np


def get_data():
    """Read CSV input from path and return the processed data

    Returns:
        (list, list): (data, labels) of processed data
    """
    data = pd.read_csv("./assets/styles.csv", error_bad_lines=False)
    # remove unrelevant columns
    data = data.drop(['productDisplayName', 'year', 'season'], axis=1)
    # remove columns containing nan values
    data = data.dropna()

    data['image'] = ["./assets/images/" + str(id) + ".jpg" for id in data.id]
    from os import listdir
    # remove entries without image
    data = data[data['image'].isin(
        ["./assets/images/" + image for image in listdir("./assets/images/")])]

    # create all possible label combinations
    labels = np.array([(master, sub, colour, gender, articleType, usage) for master, sub, colour, gender, articleType, usage in zip(data['masterCategory'].astype(
        str), data['subCategory'].astype(str), data['baseColour'].astype(str), data['gender'].astype(str), data['articleType'].astype(str), data['usage'].astype(str))])

    return (data, labels)


def decode_img(img: any, width: int, height: int) -> np.array:
    """Decode JPG to np.array of given width and height

    Args:
        img (any): Image in JPG format to be processed
        width (int): Widht of output
        height (int): Height of ouptput

    Returns:
        np.array: Converted image
    """
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_jpeg(img, channels=3)
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # resize the image to the desired size.
    return tf.image.resize(img, [width, height])


def save_encoder(path: str) -> MultiLabelBinarizer:
    """Train, persist and return the MultiLableBinarizer

    Args:
        path (str): Path of where to store the encoder

    Returns:
        MultiLabelBinarizer: Trained encoder
    """
    (data, labels) = get_data()
    # encode subCategory and baseColour into binary Array
    from sklearn.preprocessing import MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    mlb.fit(labels)

    np.save(path, mlb.classes_)

    return mlb


def prepare_data() -> tuple:
    """Do the whole data preparation - incl. data conversion and test/train split.

    Returns:
        tuple: (X_train, y_train, X_test, y_test)
    """
    (data, labels) = get_data()
    from sklearn.preprocessing import MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    mlb.fit(labels)
    y = mlb.transform(labels)

    # read and decode images
    images = [tf.io.read_file(path).numpy() for path in data.image]
    print("images read")
    # create an empty array to allocate storage --> much faster than converting a list into a numpy-array using np.array(...)
    X = np.zeros(shape=(len(images), 60, 80, 3))
    for i in range(len(images)):
        # pass encoded images into X
        X[i] = (decode_img(images[i], 60, 80))
    print("images decoded")

    # split data into training and test set
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    print("Data prep finished")

    return (X_train, y_train, X_test, y_test)