# USAGE
# Start the server:
# 	python run_keras_server.py
# Submit a request via cURL:
# 	curl -X POST -F image=@dog.jpg 'http://localhost:5000/predict'
# Submita a request via Python:
#	python simple_request.py

# import the necessary packages
from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from keras.utils.data_utils import get_file
from PIL import Image
import numpy as np
import flask
import tensorflow as tf
import io

# # initialize our Flask application and the Keras model
def load_model():
	graph = tf.get_default_graph()
	model = ResNet50(weights="imagenet")
	return model,graph



app = flask.Flask(__name__)
app.config["model"],app.config["graph"] = load_model()


def prepare_image(image, target):
	# if the image mode is not RGB, convert it
	if image.mode != "RGB":
		image = image.convert("RGB")

	# resize the input image and preprocess it
	image = image.resize(target)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = imagenet_utils.preprocess_input(image)

	# return the processed image
	return image

@app.route("/index",methods=["GET","POST"])
def index():

	return 'test'

@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view

	data = {"success": False}

	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		# model = ResNet50(weights="imagenet", include_top=True)
		if flask.request.files.get("image"):
			# read the image in PIL format
			image = flask.request.files["image"].read()
			image = Image.open(io.BytesIO(image))

			# preprocess the image and prepare it for classification
			image = prepare_image(image, target=(224, 224))

			# classify the input image and then initialize the list
			# of predictions to return to the client
			# print(model.summary())

			with app.config["graph"].as_default():
				preds = app.config["model"].predict(image)

			results = imagenet_utils.decode_predictions(preds)
			data["predictions"] = []

			# loop over the results and add them to the list of
			# returned predictions
			for (imagenetID, label, prob) in results[0]:
				r = {"label": label, "probability": float(prob)}
				data["predictions"].append(r)

			# indicate that the request was a success
			data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	# load_model()
	app.run(host='0.0.0.0')
	# app.run()