# Do not edit if deploying to Banana Serverless
# This file is boilerplate for the http server, and follows a strict interface.

# Instead, edit the init() and inference() functions in app.py

from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from flask_cors import CORS, cross_origin
import subprocess
import app as user_src


app = Flask(__name__)
CORS(app)
# We do the model load-to-GPU step on server startup
# so the model object is available globally for reuse
user_src.init()


# Healthchecks verify that the environment is correct on Banana Serverless
@app.route('/healthcheck', methods=["GET"])
def healthcheck():
    # dependency free way to check if GPU is visible
    gpu = False
    out = subprocess.run("nvidia-smi", shell=True)
    if out.returncode == 0: # success state on shell command
        gpu = True

    return {"state": "healthy", "gpu": gpu}

# Inference POST handler at '/' is called for every http call from Banana
@app.route('/', methods=["POST"]) 
def inference():
    try:
        model_inputs = request.load_json()
    except:
        model_inputs = request.json

    output = user_src.inference(model_inputs)

    return jsonify(output)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)

