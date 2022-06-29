from src.utils.all_utils import read_yaml, create_directory, load_model, error_value
import os, argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import RandomizedSearchCV, train_test_split
import xgboost as xgb
import logging
import io
from sklearn.metrics import accuracy_score



#-------------------------------------------------------------------------------
#   Creating a looging with timestamp and regex 
#-------------------------------------------------------------------------------

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'stage_05_running_logs.log'), level=logging.INFO, format=logging_str,filemode="a")

#-------------------------------------------------------------------------------
#   Testing Model 
#-------------------------------------------------------------------------------

def model_testing(model, test_data_file, graphs_dir_path):

    df = pd.read_csv(test_data_file)
    logging.info(df.head(10))
    #df.dropna(inplace= True)

    X = df.iloc[:,:-1] # removing the last column
    y = df.iloc[:,-1]
    #-----------------
    X = X.values
    y = y.values
    prediction = model.predict(X)


    logging.info(" fetched file location is : {}".format(test_data_file))
    logging.info("model.best_params_ : {}".format(model.best_params_))
    logging.info("model.best_score_ : {}".format(model.best_score_))

    sns.displot(y-prediction)
    fig = plt.figure()
    sns.distplot(y)
    fig.savefig('{}/001_TRAINED_MODEL_TESTING_SNS_DISTPLOT(Y).png'.format(graphs_dir_path))
    logging.info(" # "*20 + "SNS_DISTPLOT(Y).png   created")

    #score =accuracy_score(y,prediction)
    #logging.info(score)

    



if __name__=="__main__":

    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    parsed_args = args.parse_args()
    config_path=parsed_args.config
    config = read_yaml(parsed_args.config)

    artifacts_dir = config["artifacts"]["artifacts_dir"]
    split_data_dir = config["artifacts"]["split_data"]["split_data_dir"]
    test_data_dir = config["artifacts"]["split_data"]["test_data_dir"]
    model_dir = config["artifacts"]["model"]["model_dir"]
    graphs_dir = config["artifacts"]['reports']['graphs']['graphs_dir']
    reports_dir = config["artifacts"]['reports']['reports_dir']    
    trained_model_graph_dir = config["artifacts"]['reports']['graphs']['trained_model_graph_dir']
    test_data_file = config["artifacts"]["split_data"]["test_data_file"]
    saved_model_filename = config["artifacts"]["model"]["xgboost_reg"]

    graphs_dir_path = os.path.join(artifacts_dir,reports_dir, graphs_dir)
    model_dir_path = os.path.join(artifacts_dir, model_dir)
    trained_model_graph_dir_path = os.path.join(artifacts_dir,reports_dir, trained_model_graph_dir)
    test_data_file_path = os.path.join(artifacts_dir, split_data_dir, test_data_dir, test_data_file)
    saved_model_file_path = os.path.join(artifacts_dir, model_dir, saved_model_filename)


    try:
        logging.info("starting STAGE 05 TESTING MODEL ACCURACY")
        create_directory([os.path.join(artifacts_dir,reports_dir, trained_model_graph_dir)])
        model = load_model(saved_model_file_path)
        model_testing(model=model, test_data_file=test_data_file_path, graphs_dir_path= trained_model_graph_dir_path)
        logging.info("Stage 05 completed successfully and all the data is saved in the locals")
    except Exception as e:
        logging.info(e)
        raise e

    
    

