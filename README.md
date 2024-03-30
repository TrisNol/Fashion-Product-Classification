# Fashion Product Classification
This project is based on the following dataset containing fashion product images and their categories.
- Small dataset: https://www.kaggle.com/paramaggarwal/fashion-product-images-small
- Big dataset: https://www.kaggle.com/paramaggarwal/fashion-product-images-dataset

## Components
The project consists of three main components:

### Training Component
In this module the machine learning model used to categorize images will be trained using the provided dataset.
The main file called [app.py](./machine%20learning%20training/app.py) will train a multi-label-encoder and a TensorFlow model, exporting them for further use.

### Backend
The backend component encapsulates a FastAPI REST API used to pass images to the model for categorization. In order to use this component, the encoder and model folder of the training components including their contents have to be copied into this project.
Once the server has been started, you can pass POST-Request to the `/categories` endpoint for processing. The body must be of JSON-format and contain a base64 encoded image of the JPG format.

### Frontend
Once opened the frontend offers you two options for adding images:

1. Drag & Drop
2. Select file(s) dialog

Any added images will be base64 encoded and passed to the previously mentioned POST endpoint.