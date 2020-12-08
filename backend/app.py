from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import tensorflow as tf
import logging

import utils.ml_utils as util

model = util.getModel()
encoder = util.getEncoder()


app = Flask(__name__)
logging.basicConfig(filename='demo.log', level=logging.DEBUG)
cors = CORS(app)

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    if path.endswith(".js"): 
        return send_from_directory('./static', path, mimetype="application/javascript")
    return send_from_directory('./static', path)


@app.route('/')
def root():
  return send_from_directory('./static', 'index.html')


@app.route('/categories', methods=['POST'])
@cross_origin()
def process_image_external():
    try:
        image = util.read_process_image(request.json['path'])

        predictions = model.predict(image)
        predictions = util.transform_predictions(predictions)
        predictions = encoder.inverse_transform(predictions)

        return jsonify({'categories': predictions[0]})
    except:
        return "Bad Request", 400

if __name__ == '__main__':
    app.run(debug=True)
