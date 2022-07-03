import yaml
import os
import json
import pandas as pd
import numpy as np
from sklearn import metrics
import joblib
import logging
import time


#-------------------------------------------------------------------------------
#   read_yaml
#-------------------------------------------------------------------------------

def read_yaml(path_to_yaml: str) -> dict:
    '''
    read_yaml takes String as input and gives Dictionary as output

    Parameters
    ----------
    INPUT : path_to_yaml || String
    OUTPUT : content || Dictionary
    '''
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    logging.info(f"yaml file: {path_to_yaml} loaded successfully")
    return content
#-------------------------------------------------------------------------------
#   error_value
#-------------------------------------------------------------------------------

def error_value(model, X_test, y_test):
    '''
    error_value will take the trained model as well as the X_test and y_test values and find thir MAE, MSE, RMSE
    
    Parameters
    ----------
    Input : Model : Trained model, 
            X_test : Dataset,
            y_test : Dataset
    Output : The MAE, MSE, RMSE values will be rewrite in the Logging file
    '''
    prediction = model.predict(X_test)        
    logging.info(f"MAE: { metrics.mean_absolute_error(y_test, prediction)}" )
    logging.info(f"MSE: {metrics.mean_squared_error(y_test, prediction)}" )
    logging.info(f"RMSE: {np.sqrt(metrics.mean_squared_error(y_test, prediction))}" )

#-------------------------------------------------------------------------------
#   create_directory
#-------------------------------------------------------------------------------

def create_directory(dirs: list):
    '''
    Create_directory will allow the user to create directory 
    
    Parameters
    ----------
    Input : Take list as input containing Directories name
    Output : The mentioned directories will be created
    '''
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"directory is created at {dir_path}")

#-------------------------------------------------------------------------------
#   save_local_df
#-------------------------------------------------------------------------------

def save_local_df(data, data_path, index_status=False):
    '''
    save_local_df will allow the user to save their data to their csv file in their designated location mentioned in data_path
    
    Parameters
    ----------
    INPUT : data,
            data_path(location of data to be stored)
    Output : New data is saved in the mentioned location in csv format
    '''
    data.to_csv(data_path, index=index_status)
    logging.info(f"data is saved at {data_path}")

#-------------------------------------------------------------------------------
#   save_reports
#-------------------------------------------------------------------------------

def save_reports(report: dict, report_path: str, indentation=4):
    '''
    save_reports allows users to save their reports at their designated location as mentioned in the report_path variable
    
    Parameters
    ----------
    INPUT : report : varible storing the reports  || DICT,
            report_path : location to store the reports || STRING,
            indentation :allows better readibility
    Output : The reports are saved at the mentioned location
    '''
    with open(report_path, "w") as f:
        json.dump(report, f, indent=indentation)
    logging.info(f"reports are saved at {report_path}")
#-------------------------------------------------------------------------------
#   fetch_reports
#-------------------------------------------------------------------------------
def fetch_reports(report_path: str):
    '''
    fetch_report allows users to fetch report saved at the location mentioned in the report_path variable
    
    Parameters
    ----------
    INPUT : report_path : STRING 
    OUTPUT : report : JSON format 
    '''
    with open(report_path, "w") as f:
        report = json.load(f)
    logging.info(f"reports are loaded from {report_path}")
    return report

#-------------------------------------------------------------------------------
#   Saving_model
#-------------------------------------------------------------------------------

def save_model(model_dir_path: list, model, model_filename):
    '''
    save_model allows user to save a trained model to a given location
    
    Parameters
    ----------
    INPUT : model_dir_path : containg list of directories/location, 
            model : trained model, 
            model_filename: Name of the model
    OUTPUT : model is saved at the given location with the specified model file name
    
    '''
    create_directory([model_dir_path])
    model_path = os.path.join(model_dir_path, model_filename)
    joblib.dump(model, model_path)
    logging.info(" {} save at {}".format(model_filename, model_dir_path ))

#-------------------------------------------------------------------------------
#   Loading_model
#-------------------------------------------------------------------------------
def load_model(model_file_path):
    '''
    load_model allows user to load a pretrained model stored locally in the mentioned location
    
    Parameters
    ----------
    INPUT : location of the pretrained model
    OUTPUT : the pretrained model will be loaded
    '''
    model = joblib.load(model_file_path)
    logging.info("{} file is loaded".format(model_file_path))
    return model


#-------------------------------------------------------------------------------
#   time_stamp
#-------------------------------------------------------------------------------
def get_timestamp(name):
    '''
    it will create a unique name using the timestamp 

    Parameters
    ----------
    INPUT : Name || String
    OUTPUT : unique_name || String
    '''
    timestamp = time.asctime().replace(" ", "_").replace(":", "_")
    unique_name = f"{name}_at_{timestamp}"
    return unique_name