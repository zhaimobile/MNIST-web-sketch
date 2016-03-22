from flask import Flask, request, send_file, redirect
import json
import os
import numpy as np
from numpy import array
from skimage.measure import block_reduce
import sketchNetwork as net
from sketchNetwork import draw
from numpyEncoder import *


CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
NET_DIM = 29
HIDDEN_LAYERS = 30
OUTPUTS = 10

# instantiate neural network
net = net.Network([NET_DIM*NET_DIM, HIDDEN_LAYERS, OUTPUTS])
# create Flask server
app = Flask(__name__, static_path = '/static')

@app.route("/sketch", methods=["POST", "GET"])
def sketch():
	data = request.get_json()
	print len(data)
	a = array(data).reshape(400,400)
	print a.shape
	a = block_reduce(a, block_size=(14,14), func=np.mean)
	a = a[1:,1:]
	a = a.reshape((784,1))
	print a.shape

	# forward propagate to get the guess by the network
	f = open("parametersL2W.json", "r")
	weights = json.load(f, object_hook=json_numpy_obj_hook)

	h = open("biasesL2W.json", "r")
	biases = json.load(h, object_hook=json_numpy_obj_hook)

	res = net.bingo(a, biases, weights)
	# print res
	res = np.argmax(res)
	print res, 'yo'

	# make neurel net, pass in data
	return "res"

@app.route("/")
def root():
	return redirect('static/sketch.html')

# def block_mean(data, fact):
#     assert isinstance(fact, int), type(fact)
#     sx, sy = ar.shape
#     X, Y = np.ogrid[0:sx, 0:sy]
#     regions = sy/fact * (X/fact) + Y/fact
#     res = ndimage.mean(ar, labels=regions, index=np.arange(regions.max() + 1))
#     res.shape = (sx/fact, sy/fact)
#     return res

if __name__ == "__main__":
	app.run(debug=True)


