from src.utils.all_utils import read_yaml, create_directory, save_model, error_value, save_reports
import os, argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import RandomizedSearchCV, train_test_split
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def evaluate_metrics(actual_values, predicted_values):
    rmse = np.sqrt(mean_squared_error(actual_values, predicted_values))
    mae = mean_absolute_error(actual_values, predicted_values)
    r2 = r2_score(actual_values, predicted_values)
    return rmse, mae, r2



def model_traininig(params, train_data_file_path, scores_dir_path):    
        
    #--------------------------------------------------------------------------------------------------------
    #  ARRANGING DATA
    #--------------------------------------------------------------------------------------------------------
    df = pd.read_csv("{}".format(train_data_file_path))
    print(df.head(10))
    #df.dropna(inplace= True)

    X = df.iloc[:,:-1] # removing the last column
    y = df.iloc[:,-1]
    #--------------------------------------------------------------------------------------------------------
    #  FETCHING PARAMETERS
    #--------------------------------------------------------------------------------------------------------
    
    random_state = params["split_data"]["random_state"]
    test_size = params["split_data"]["test_size"]
    
    n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
    max_depth = [int(x) for x in np.linspace(5, 30, num = 6)]

    learning_rate = params["xg_boost"]["learning_rate"]
    subsample = params["xg_boost"]["subsample"]
    min_child_weight = params["xg_boost"]["min_child_weight"]

    params = {'n_estimators': n_estimators,
               'learning_rate': learning_rate,
               'max_depth': max_depth,
               'subsample': subsample,
               'min_child_weight': min_child_weight}
    
    #--------------------------------------------------------------------------------------------------------
    #  MODEL TRAINING WITH RandomizedSearchCV  HYPER-PARAMETER TUNING
    #--------------------------------------------------------------------------------------------------------
    X = X.values
    y = y.values
    X_train, X_test, y_train , y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    regressor = xgb.XGBRegressor()
    #regressor.fit(X_train, y_train)
    #prediction = regressor.predict(X_test)
    
    xgb_random = RandomizedSearchCV(estimator= regressor,
        param_distributions= params ,
        n_iter=50,
        scoring="neg_mean_squared_error", 
        cv=5,
        n_jobs=1 ,
        verbose=2,
        random_state=42)

    
    xgb_random.fit(X_train ,y_train) 
    #--------------------------------------------------------------------------------------------------------
    #  PRINTING AND SAVING SCORES AND ERRORS
    #--------------------------------------------------------------------------------------------------------

    predicted_values = xgb_random.predict(X_test)
    rmse, mae, r2 = evaluate_metrics(y_test, predicted_values)

    xgb_random_best_params_  = xgb_random.best_params_
    xgb_random_best_score_  = xgb_random.best_score_
    
    scores = {
        "xgb_random.best_params_ ": xgb_random_best_params_,
        "xgb_random.best_score_ ": xgb_random_best_score_ ,
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
    }

    save_reports(report=scores, report_path=scores_filepath)

    #print('MAE:', metrics.mean_absolute_error(y_test, prediction))
    #print('MSE:', metrics.mean_squared_error(y_test, prediction))
    #print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, prediction)))

    error_value(xgb_random, X_test, y_test)
       
   
    return xgb_random


    

if __name__=="__main__":

    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()
    config_path=parsed_args.config

    config = read_yaml(parsed_args.config)
    params = read_yaml(parsed_args.params)

    #--------------------------------------------------------------------------------------------------------
    #  fetching file locations
    #--------------------------------------------------------------------------------------------------------


    artifacts_dir = config["artifacts"]["artifacts_dir"]
    split_data_dir = config["artifacts"]["split_data"]["split_data_dir"]
    train_data_dir = config["artifacts"]["split_data"]["train_data_dir"]
    model_dir = config["artifacts"]["model"]["model_dir"]
    

    model_dir_path = os.path.join(artifacts_dir, model_dir)
    create_directory([model_dir_path])

    train_data_file = config["artifacts"]["split_data"]["train_data_file"]
    saved_model_filename = config["artifacts"]["model"]["xgboost_reg"]

    train_data_file_path = os.path.join(artifacts_dir, split_data_dir,train_data_dir, train_data_file )
    saved_model_file_path = os.path.join(artifacts_dir, model_dir, model_dir_path)

    scores_dir = config["artifacts"]["reports"]["reports_dir"]
    scores_filename = config["artifacts"]["reports"]["scores"]

    scores_dir_path = os.path.join(artifacts_dir, scores_dir)

    create_directory([scores_dir_path])

    scores_filepath = os.path.join(scores_dir_path, scores_filename)

    #--------------------------------------------------------------------------------------------------------
    #  PRINTING SCORES AND ERRORS
    #--------------------------------------------------------------------------------------------------------
    
    model = model_traininig(params, train_data_file_path, scores_filepath)
    # saving model
    save_model(model_dir_path, model, saved_model_filename)




    