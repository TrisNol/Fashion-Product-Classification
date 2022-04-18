from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import logging

import utils.ml_utils as util

model = util.getModel(path="./model/")
encoder = util.getEncoder(path="./encoder/classes.npy")


app = Flask(__name__)
logging.basicConfig(filename='demo.log', level=logging.DEBUG)
cors = CORS(app)

# @app.route('/<path:path>', methods=['GET'])
# def static_proxy(path):
#     if path.endswith(".js"): 
#         return send_from_directory('./static', path, mimetype="application/javascript")
#     return send_from_directory('./static', path)


# @app.route('/')
# def root():
#   return send_from_directory('./static', 'index.html')


@app.route('/categories', methods=['POST'])
@cross_origin()
def process_image_external():
    try:
        # get base64 encoded image transformed
        image = util.decode_img(request.json['image'])

        predictions = model.predict(image)
        predictions = util.transform_predictions(predictions)
        predictions = encoder.inverse_transform(predictions)

        return jsonify({'categories': predictions[0]})
    except Exception as e:
        print(e)
        return "Bad Request", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
