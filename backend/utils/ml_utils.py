import base64
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MultiLabelBinarizer

def getEncoder(path: str) -> MultiLabelBinarizer:
    """Read the multi-label encoder used for the dataset from the given path.

    Args:
        path (str): Path to the persisted encoder classes

    Returns:
        MultiLabelBinarizer: Encoder
    """
    encoder = MultiLabelBinarizer()
    encoder.classes_ = np.load(path, allow_pickle=True)
    return encoder

def getModel(path: str) -> tf.keras.Model:
    """Read the TF model from the given path

    Args:
        path (str): Path to the persisted model 

    Returns:
        tf.keras.Model: TF Model
    """
    return tf.keras.models.load_model(path)

def decode_img(img: str, width: int=60, height: int=80) -> np.array:
    """Convert a Base64 encoded image to a numpy-array

    Args:
        img (str): Base64 encoded image
        width (int, optional): Widht of output image. Defaults to 60.
        height (int, optional): Height of output image. Defaults to 80.

    Returns:
        np.array: Array represenation of image
    """
    img = base64.b64decode(img)
    nparr = np.fromstring(img, np.uint8)
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_jpeg(img, channels=3)
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # resize the image to the desired size.
    return np.array(tf.image.resize(img, [width, height])).reshape((1, 60, 80, 3))

def transform_predictions(predictions: list, threshhold: float=0.6) -> np.array:
    """Reshape predictions to binary matrix based on threshhold

    Args:
        predictions (list): Predictions of model
        threshhold (float, optional): Percentage theshhold. Defaults to 0.6.

    Returns:
        np.array: Transformed predictions as binary array
    """
    predictions = [1 if (elem > threshhold).any() else 0 for elem in predictions[0]]
    temp = []
    temp.append(np.array(predictions).reshape(-1,1).flatten())
    predictions = np.array(temp)
    return predictions
