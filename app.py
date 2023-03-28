from flask import Flask, render_template, request
from flask_cors import cross_origin
from src.utils.all_utils import read_yaml, load_model
from src.utils.databse import create_database, save_to_database
import json
import os
import numpy as np

#-------------------------------------------------------------------------------
#   loading model from local
#-------------------------------------------------------------------------------

config = read_yaml("config/config.yaml")

artifacts_dir = config["artifacts"]["artifacts_dir"]
model_dir = config["artifacts"]["model"]["model_dir"]
reports_dir = config["artifacts"]["reports"]["reports_dir"]

scores_filename = config["artifacts"]["reports"]["scores"]
saved_model_filename = config["artifacts"]["model"]["xgboost_reg"]

database_name = config["artifacts"]["reports"]["database_name"]

saved_model_file_path = os.path.join(artifacts_dir, model_dir, saved_model_filename)
scores_file_path = os.path.join(artifacts_dir, reports_dir, scores_filename)
db_file_path = os.path.join(artifacts_dir, reports_dir, database_name)

model = load_model(saved_model_file_path)
print("model loaded")

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

model_report = fetch_reports(scores_file_path)

#-------------------------------------------------------------------------------
# DMT_PREDICT
#-------------------------------------------------------------------------------

@app.route("/dem_predict", methods=["POST"])
def dmt_predict():
    try:
        visit = float(request.form["visit"])
        mr_delay = float(request.form["mr_delay"])
        Age = float(request.form["Age"])
        EDUC = float(request.form["EDUC"])
        SES = float(request.form["SES"])
        CDR = float(request.form["CDR"])
        eTIV = float(request.form["eTIV"])
        nWBV = float(request.form["nWBV"])
        gender = float(request.form["Gender"])
        ASF = float(request.form["ASF"])
        MMSE = float(request.form["MMSE"])

        data = [visit, mr_delay, Age, EDUC, SES, MMSE, CDR, eTIV, nWBV, ASF, gender]
        Xnew = np.array(data).reshape((1, -1))

        output = model.predict(Xnew)
        y_pred = [0 if i < 0.6 else 1 for i in output]
        save_to_database(db_file_path, visit, mr_delay, Age, EDUC, SES, CDR, eTIV, nWBV, gender, ASF, MMSE, y_pred[0])
        
        
        if y_pred[0] == 1:
            return "Person is demented and needs medical attention"
        else:
            return "Person is not demented"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

if __name__ == "__main__":
    try:
        create_database(db_file_path)
    except Exception as e:
        print(e)
    app.run(debug=True, host="127.0.0.1", port=5000)
