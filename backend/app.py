import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import utils.ml_utils as util
from models.Categories import Categories
from models.ImageModel import ImageModel

model = util.getModel(path="./model/")
encoder = util.getEncoder(path="./encoder/classes.npy")


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(filename='demo.log', level=logging.DEBUG)

@app.post('/categories')
def categorize_image(image: ImageModel) -> Categories:
    """Categorize an image into multiple product categories using TensorFlow.

    Args:
        image (ImageModel): Base64 encoded JPG image

    Raises:
        HTTPException: Request could not be processed (e.g. wrong image format)

    Returns:
        Categories: Identified labels
    """
    try:
        # get base64 encoded image transformed
        image = util.decode_img(image.image)

        predictions = model.predict(image)
        predictions = util.transform_predictions(predictions)
        predictions = encoder.inverse_transform(predictions)

        return Categories(categories=predictions[0])
    except Exception as e:
        raise HTTPException(400)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
