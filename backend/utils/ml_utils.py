import tensorflow as tf
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import requests


def getEncoder():
    encoder = MultiLabelBinarizer()
    encoder.classes_ = np.load("./encoder/classes.npy", allow_pickle=True)
    return encoder

def getModel():
    return tf.keras.models.load_model('./model/')

def read_process_image(path):
    image = [[decode_img(requests.get(path).content, 60, 80)]]
    return image

def decode_img(img, width, height):
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_jpeg(img, channels=3)
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # resize the image to the desired size.
    return tf.image.resize(img, [width, height])

def transform_predictions(predictions):
    predictions = [1 if (elem > 0.60).any() else 0 for elem in predictions[0]]
    temp = []
    temp.append(np.array(predictions).reshape(-1,1).flatten())
    predictions = np.array(temp)
    return predictions
