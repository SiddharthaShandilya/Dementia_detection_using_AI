from __future__ import division, print_function
# Flask utils
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

from flask_cors import cross_origin
from src.utils.all_utils import read_yaml, load_model,create_directory
import json
import os, logging
import numpy as np

# coding=utf-8

import numpy as np
import tensorflow as tf
# Keras
# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model as load_deep_model
from tensorflow.keras.preprocessing import image

import numpy as np
import tensorflow as tf


#-------------------------------------------------------------------------------
#   Creating a looging with timestamp and regex 
#-------------------------------------------------------------------------------

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'stage_06_flask_running_logs.log'), level=logging.INFO, format=logging_str,filemode="a")
logging.info(f"\n\n")


#-------------------------------------------------------------------------------
#   loading model from local
#-------------------------------------------------------------------------------

#config_path="config/config.yaml"
config = read_yaml("config/config.yaml")

artifacts_dir = config["artifacts"]["artifacts_dir"]
model_dir = config["artifacts"]["model"]["model_dir"]
reports_dir = config["artifacts"]["reports"]["reports_dir"]

web_app_upload_dir = config["web_app"]["upload_folder"]

scores_filename = config["artifacts"]["reports"]["scores"]
saved_deep_model_filename = config["artifacts"]["model"]["finalized_model"]
#saved_model_filename = config["artifacts"]["model"]["logistic_reg_model"]
saved_model_filename = config["artifacts"]["model"]["xgboost_reg"]

saved_model_file_path = os.path.join(artifacts_dir, model_dir, saved_model_filename)
saved_deep_model_file_path = os.path.join(artifacts_dir, model_dir, saved_deep_model_filename)
scores_file_path = os.path.join(artifacts_dir, reports_dir, scores_filename)



#-------------------------------------------------------------------------------
#   Creating flask app
#-------------------------------------------------------------------------------
app = Flask(__name__)

#-------------------------------------------------------------------------------
#   fetch_reports
#-------------------------------------------------------------------------------
def fetch_reports(report_path: str):
    with open(report_path, "r") as f:
        report = json.load(f)
    logging.info(f"reports are loaded from {report_path}")
    logging.info(report)
    return report


#-------------------------------------------------------------------------------
# DMT_ML_PREDICT
#-------------------------------------------------------------------------------

@app.route("/dem_predict",methods = ["GET", "POST"])
def aqt_predict():

    logging.info(f"Loading Machine Learning model from filepath {saved_model_file_path}")
    model = load_model(saved_model_file_path)
    logging.info(f"model loaded from filepath {saved_model_file_path}")
    #logging.info(f"model evaluation : {mo}"
    model_report =  fetch_reports(scores_file_path)

    if request.method == "POST":
               
        visit = float(request.form["visit"])
        mr_delay = float(request.form["mr_delay"])
        Age = float(request.form["Age"])
        EDUC = float(request.form["EDUC"])
        SES = float(request.form["SES"])
        CDR = float(request.form["CDR"])
        eTIV = float(request.form["eTIV"])
        nWBV = float(request.form["nWBV"])
        gender = float(request.form["Gender"])
        ASF  = float(request.form["ASF"])
        MMSE   = float(request.form["MMSE"])


        data = [visit, mr_delay ,Age , EDUC, SES, MMSE, CDR,eTIV, nWBV, ASF, gender]

        #data = [const, gender, Age,  EDUC , SES  ,eTIV ,    nWBV , ASF , MMSE , CDR]
        #data = [const, EDUC, SES, nWBV, ASF, MMSE, CDR]

        for i in data:
            logging.info(f"Printing the type of data in the recieved data {type(i)}")

        Xnew = np.array(data).reshape((1,-1))

        for i in Xnew:
            logging.info(f"Xnew type si {i}")

        #print(" \n\n" )
        logging.info(Xnew)
        #print(" \n\n" )

        output = model.predict(Xnew)
        print("ouyput",output)
        y_pred=[0 if i<0.6 else 1 for i in output]
        print("ouyput",y_pred)
        
        if (y_pred[0] == 1):
            print("True == ",y_pred)
            return " Person is demented and need medical attention"
        
        print("False == ",y_pred)
        return " person in not demetned"
        


#-------------------------------------------------------------------------------
# DMT_Deep_learning_PREDICT
#-------------------------------------------------------------------------------


def model_predict(img_path, load_model):
    img = image.load_img(img_path, target_size=(150, 150))
    logging.info(f" the type of object uploaded  : {type(img)}")
    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)
    #logging.info(f" The shape of image uploaded : {x.shape()}")
    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='caffe')

    preds = load_model.predict(x, batch_size=None, verbose=0, steps=None, callbacks=None)
    return preds



@app.route('/predict', methods=['GET', 'POST'])
def upload():
    logging.info(f"loading Deep Learning model from ../Alzheimer_model_latest.h5 ")
    deep_model = load_deep_model("../Alzheimer_model_latest.h5")
    logging.info(' deep_learning Model loaded. Start serving...')
    logging.info('deep_model loaded. Check http://127.0.0.1:5000/')
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        create_directory([web_app_upload_dir])
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        logging.info(f" The location of uploaded image is : {file_path}")
        #PIL.Image.open(str(roses[0]))

        # Make prediction
        IMAGE_SIZE = [150,150]
        preds = model_predict(file_path, deep_model)

        # Process your result for human
        #pred_class = preds.argmax(axis=-1)            # Simple argmax
        #test_ds = tf.keras.preprocessing.image_dataset_from_directory("artifacts/Data_archive/alzheimers_dataset/test", image_size=IMAGE_SIZE,)
        #pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        #result = str(pred_class[0][0][1])               # Convert to string
        #result = str(pred_class)
        result  = preds
        print(f"\n{result}\n")
        #os.remove(file_path)
        return str(np.argmax(result))
    return None


###############################################################################################################


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

if __name__ == "__main__":
    #aqt_predict()
    try:
        logging.info("Starting 06 Flask application ")
        app.run(debug = True, host='127.0.0.1', port=5000)
        logging.info("Stage 06 completed successfully ")
    except Exception as e:
        logging.info(e)
        raise e
    
