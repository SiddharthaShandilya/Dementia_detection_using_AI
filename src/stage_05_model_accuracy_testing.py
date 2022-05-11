

from src.utils.all_utils import read_yaml, create_directory, load_model, error_value
import os, argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import RandomizedSearchCV, train_test_split
import xgboost as xgb

from sklearn.metrics import accuracy_score



def model_testing(model, test_data_file, graphs_dir_path):

    df = pd.read_csv(test_data_file)
    print(df.head(10))
    #df.dropna(inplace= True)

    X = df.iloc[:,:-1] # removing the last column
    y = df.iloc[:,-1]
    #-----------------
    X = X.values
    y = y.values
    prediction = model.predict(X)


    print(" fetched file location is : {}".format(test_data_file))
    print("model.best_params_ : {}".format(model.best_params_))
    print("model.best_score_ : {}".format(model.best_score_))

    sns.displot(y-prediction)
    fig = plt.figure()
    sns.distplot(y)
    fig.savefig('{}/001_TRAINED_MODEL_TESTING_SNS_DISTPLOT(Y).png'.format(graphs_dir_path))
    print(" # "*20 + "SNS_DISTPLOT(Y).png   created")

    #score =accuracy_score(y,prediction)
    #print(score)

    



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
   
    graphs_dir_path = os.path.join(artifacts_dir,reports_dir, graphs_dir)
    model_dir_path = os.path.join(artifacts_dir, model_dir)
    
    trained_model_graph_dir_path = os.path.join(artifacts_dir,reports_dir, trained_model_graph_dir)

    create_directory([os.path.join(artifacts_dir,reports_dir, trained_model_graph_dir)])

    test_data_file = config["artifacts"]["split_data"]["test_data_file"]
    saved_model_filename = config["artifacts"]["model"]["xgboost_reg"]

    test_data_file_path = os.path.join(artifacts_dir, split_data_dir, test_data_dir, test_data_file)
    saved_model_file_path = os.path.join(artifacts_dir, model_dir, saved_model_filename)

    model = load_model(saved_model_file_path)
    model_testing(model=model, test_data_file=test_data_file_path, graphs_dir_path= trained_model_graph_dir_path)

    
    

