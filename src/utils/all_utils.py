import yaml
import os
import json
import pandas as pd
import numpy as np
from sklearn import metrics
import joblib


#-------------------------------------------------------------------------------
#   read_yaml
#-------------------------------------------------------------------------------

def read_yaml(path_to_yaml: str) -> dict:
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)

    return content
#-------------------------------------------------------------------------------
#   error_value
#-------------------------------------------------------------------------------

def error_value(model, X_test, y_test):
    prediction = model.predict(X_test)        
    print('MAE:', metrics.mean_absolute_error(y_test, prediction))
    print('MSE:', metrics.mean_squared_error(y_test, prediction))
    print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, prediction)))

#-------------------------------------------------------------------------------
#   create_directory
#-------------------------------------------------------------------------------

def create_directory(dirs: list):
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"directory is created at {dir_path}")

#-------------------------------------------------------------------------------
#   save_local_df
#-------------------------------------------------------------------------------

def save_local_df(data, data_path, index_status=False):
    data.to_csv(data_path, index=index_status)
    print(f"data is saved at {data_path}")

#-------------------------------------------------------------------------------
#   save_reports
#-------------------------------------------------------------------------------

def save_reports(report: dict, report_path: str, indentation=4):
    with open(report_path, "w") as f:
        json.dump(report, f, indent=indentation)
    print(f"reports are saved at {report_path}")
#-------------------------------------------------------------------------------
#   fetch_reports
#-------------------------------------------------------------------------------
def fetch_reports(report_path: str):
    with open(report_path, "w") as f:
        report = json.load(f)
    print(f"reports are loaded from {report_path}")
    return report

#-------------------------------------------------------------------------------
#   Saving_model
#-------------------------------------------------------------------------------

def save_model(model_dir_path: list, model, model_filename):
    
    create_directory([model_dir_path])
    model_path = os.path.join(model_dir_path, model_filename)
    joblib.dump(model, model_path)
    print(" {} save at {}".format(model_filename, model_dir_path ))

#-------------------------------------------------------------------------------
#   Loading_model
#-------------------------------------------------------------------------------
def load_model(model_file_path):
    model = joblib.load(model_file_path)
    print("{} file is loaded".format(model_file_path))
    return model


#-------------------------------------------------------------------------------
#   avg_data
#-------------------------------------------------------------------------------

def avg_data(aqi_data_dir_path,year):
    
    temp_i=0
    average=[]
    for rows in pd.read_csv("{}/aqi{}.csv".format(aqi_data_dir_path,year), chunksize=24):
#    for rows in pd.read_csv("data/AQI/aqi2014.csv", chunksize=24):

        add_var=0
        data=[]
        avg=0.0
        df=pd.DataFrame(data=rows)
        for index, rows in df.iterrows():
            data.append(rows['PM2.5'])
            #count=
        for i in data:
            if type(i) is float or type(i) is int:
                add_var=add_var+i
                    #count=count+1
            elif type(i) is str:
                if i!="NoData" and i!="PwrFail" and i!="---" and i!="InVld":
                    temp=float(i)
                    add_var=add_var+temp
                    #count=count+1
        avg = add_var/24   #count
        temp_i=temp_i+1
        average.append(avg)

        
    return average
