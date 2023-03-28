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
    Reads a YAML file and returns its contents as a dictionary.

    Parameters
    ----------
    path_to_yaml : str
        The path to the YAML file.

    Returns
    -------
    dict
        The contents of the YAML file as a dictionary.
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
    Calculates the Mean Absolute Error (MAE), Mean Squared Error (MSE), and Root
    Mean Squared Error (RMSE) of a trained model using a test dataset.

    Parameters
    ----------
    model : object
        The trained model.
    X_test : array-like
        The test dataset.
    y_test : array-like
        The target values for the test dataset.

    Returns
    -------
    None
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
    Creates one or more directories.

    Parameters
    ----------
    dirs : list
        A list of directory names to be created.

    Returns
    -------
    None
    '''
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"directory is created at {dir_path}")

#-------------------------------------------------------------------------------
#   save_local_df
#-------------------------------------------------------------------------------

def save_local_df(data, data_path, index_status=False):
    '''
    Saves a Pandas DataFrame to a CSV file.

    Parameters
    ----------
    data : Pandas DataFrame
        The data to be saved.
    data_path : str
        The path to the file where the data will be saved.
    index_status : bool, optional
        Whether to include the index column in the saved data. The default is False.

    Returns
    -------
    None
    '''
    data.to_csv(data_path, index=index_status)
    logging.info(f"data is saved at {data_path}")

#-------------------------------------------------------------------------------
#   save_reports
#-------------------------------------------------------------------------------

def save_reports(report: dict, report_path: str, indentation=4):
    '''
    Saves a dictionary as a JSON file.

    Parameters
    ----------
    report : dict
        The dictionary to be saved.
    report_path : str
        The path to the file where the dictionary will be saved.
    indentation : int, optional
        The number of spaces to use for indentation in the saved JSON file. The default is 4.

    Returns
    -------
    None
    '''

    with open(report_path, "w") as f:
        json.dump(report, f, indent=indentation)
    logging.info(f"reports are saved at {report_path}")
#-------------------------------------------------------------------------------
#   fetch_reports
#-------------------------------------------------------------------------------
def fetch_reports(report_path: str):
    """
    Load the report from the specified path.

    Parameters
    ----------
    report_path : str
        The path to the report file in JSON format.

    Returns
    -------
    dict
        A dictionary containing the report data.
    """
    with open(report_path, "w") as f:
        report = json.load(f)
    logging.info(f"reports are loaded from {report_path}")
    return report

#-------------------------------------------------------------------------------
#   Saving_model
#-------------------------------------------------------------------------------

def save_model(model_dir_path: list, model, model_filename):
    """
    Save a trained model to a specified location.

    Parameters
    ----------
    model_dir_path : str
        The path to the directory where the model will be saved.
    model : object
        The trained model object.
    model_filename : str
        The filename to be used for the saved model.

    Returns
    -------
    None
    """
    create_directory([model_dir_path])
    model_path = os.path.join(model_dir_path, model_filename)
    joblib.dump(model, model_path)
    logging.info(" {} save at {}".format(model_filename, model_dir_path ))

#-------------------------------------------------------------------------------
#   Loading_model
#-------------------------------------------------------------------------------
def load_model(model_file_path):
    """
    Load a pretrained model from a specified location.

    Parameters
    ----------
    model_file_path : str
        The path to the pretrained model file.

    Returns
    -------
    object
        The pretrained model object.
    """
    model = joblib.load(model_file_path)
    logging.info("{} file is loaded".format(model_file_path))
    return model


#-------------------------------------------------------------------------------
#   time_stamp
#-------------------------------------------------------------------------------
def get_timestamp(name):
    """
    Generate a unique name using a timestamp.

    Parameters
    ----------
    name : str
        The name to be used in the generated unique name.

    Returns
    -------
    str
        A unique name generated using a timestamp.
    """
    timestamp = time.asctime().replace(" ", "_").replace(":", "_")
    unique_name = f"{name}_at_{timestamp}"
    return unique_name