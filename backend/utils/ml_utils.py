import tensorflow as tf
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np
import cv2
import base64


def getEncoder(path: str):
    encoder = MultiLabelBinarizer()
    encoder.classes_ = np.load(path, allow_pickle=True)
    return encoder

def getModel(path: str):
    return tf.keras.models.load_model(path)

def decode_img(img, width=60, height=80):
    img = base64.b64decode(img)
    nparr = np.fromstring(img, np.uint8)
    print(nparr.shape)
    # img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_jpeg(img, channels=3)
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # resize the image to the desired size.
    return np.array(tf.image.resize(img, [width, height])).reshape((1, 60, 80, 3))

def transform_predictions(predictions):
    predictions = [1 if (elem > 0.60).any() else 0 for elem in predictions[0]]
    temp = []
    temp.append(np.array(predictions).reshape(-1,1).flatten())
    predictions = np.array(temp)
    return predictions
