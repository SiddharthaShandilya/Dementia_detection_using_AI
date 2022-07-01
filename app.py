from flask import Flask, render_template, request
from flask_cors import cross_origin
from src.utils.all_utils import read_yaml, load_model
import json
import os
import numpy as np
import pickle



#-------------------------------------------------------------------------------
#   loading model from local
#-------------------------------------------------------------------------------

#config_path="config/config.yaml"
config = read_yaml("config/config.yaml")

artifacts_dir = config["artifacts"]["artifacts_dir"]
model_dir = config["artifacts"]["model"]["model_dir"]
reports_dir = config["artifacts"]["reports"]["reports_dir"]

scores_filename = config["artifacts"]["reports"]["scores"]
#saved_model_filename = config["artifacts"]["model"]["finalized_model"]
#saved_model_filename = config["artifacts"]["model"]["logistic_reg_model"]
saved_model_filename = config["artifacts"]["model"]["xgboost_reg"]

saved_model_file_path = os.path.join(artifacts_dir, model_dir, saved_model_filename)
scores_file_path = os.path.join(artifacts_dir, reports_dir, scores_filename)

model = load_model(saved_model_file_path)
print(" model loaded")



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
    print(f"reports are loaded from {report_path}")
    print(report)
    return report


#-------------------------------------------------------------------------------
# DMT_PREDICT
#-------------------------------------------------------------------------------

@app.route("/dem_predict",methods = ["GET", "POST"])
def aqt_predict():

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
            print(type(i))

        Xnew = np.array(data).reshape((1,-1))

        for i in Xnew:
            print("Xnew type si ",i)

        print(" \n\n" )
        print(Xnew)
        print(" \n\n" )

        output = model.predict(Xnew)
        print("ouyput",output)
        y_pred=[0 if i<0.6 else 1 for i in output]
        print("ouyput",y_pred)
        #out = " "
        #'''
        if (y_pred[0] == 1):
            print("True == ",y_pred)
            return " Person is demented and need medical attention"
        
        print("False == ",y_pred)
        return " person in not demetned"
        
        #'''
       
        #return "<p>model fetched from \t\t {}</p>" .format(output)


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

if __name__ == "__main__":
    #aqt_predict()
    app.run(debug = True, host='127.0.0.1', port=5000)
    