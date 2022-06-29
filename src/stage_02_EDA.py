import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse, os
from src.utils.all_utils import create_directory, read_yaml, save_local_df
from sklearn.ensemble import ExtraTreesRegressor
import logging

#-------------------------------------------------------------------------------
#   Creating a looging with timestamp and regex 
#-------------------------------------------------------------------------------

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'stage_02_running_logs.log'), level=logging.INFO, format=logging_str,filemode="a")


#-------------------------------------------------------------------------------
#                          EDA FUNCTION
#-------------------------------------------------------------------------------

def eda(config_path):

    config = read_yaml(config_path)

    artifacts_dir = config["artifacts"]['artifacts_dir'] # points to artifacts folder
    data_local_dir = config["artifacts"]['data_local_dir'] # points to data folder inside artifacts
    raw_data_dir = config["artifacts"]['raw_data_dir'] # points to Real-Data folder(DEMENTIA DATASET) inside artifacts/raw_data

    real_data_dir = config["artifacts"]['real_data_dir'] # points to Real-Data folder inside artifacts/data
    real_data_combined_file = config["artifacts"]['real_data_combined_file'] # points to  Real_Combine.csv 
    cleaned_real_data_file = config["artifacts"]['cleaned_real_data_file'] # points to  cleaned_real_data_file.csv 

    reports_dir = config["artifacts"]['reports']['reports_dir']
    graphs_dir = config["artifacts"]['reports']['graphs']['graphs_dir']
    graphs_dir_path = os.path.join(artifacts_dir,reports_dir, graphs_dir)


    real_data_combined_file_path = os.path.join(artifacts_dir, data_local_dir, raw_data_dir, real_data_combined_file)

    cleaned_real_data_file_path = os.path.join(artifacts_dir, data_local_dir, real_data_dir, cleaned_real_data_file)

    #creating directory .\artifacts\data\real_data
    cleaned_data_path  = os.path.join(artifacts_dir, data_local_dir, real_data_dir)
    create_directory([cleaned_data_path]) 

    #data = eda(real_data_combined_file_path)
    logging.info(f" real_data_combined_file_path = {format(real_data_combined_file_path)}")
    
    df = pd.read_csv(real_data_combined_file_path) 
    logging.info(" FILE LOCATION : {}".format(real_data_combined_file_path))
    #logging.info(df)
    
    #------------------------------------------------------------------------------- 
    #                               removing dummy variables    
    #------------------------------------------------------------------------------- 
    df = pd.get_dummies(df, columns=['M/F', 'Group','Hand'], drop_first=True)
    df.dropna(inplace= True)
    #Removing unwanted columnms such as id or Group_Nondemented as Group_demented is already present
    X = df.drop(labels=['MRI ID','Subject ID','Group_Nondemented','Group_Demented'], axis=1)
    y = df['Group_Demented']

    # finding co- relation
    corr_mat = df.corr()
    top_corr_features = corr_mat.index
    logging.info("top_corr_features = {}".format(top_corr_features))

    
    #-------------------------------------------------------------------------------
    #                          feature importance  
    #-------------------------------------------------------------------------------

    model = ExtraTreesRegressor()
    model.fit(X,y)
    logging.info("model.feature_importances_ = {}".format(model.feature_importances_))

    #-------------------------------------------------------------------------------
    #                           UPLOADING GRAPHS   
    #-------------------------------------------------------------------------------
    if not os.path.exists("{}".format(graphs_dir_path)):
        create_directory([os.path.join(os.path.join(artifacts_dir, reports_dir, graphs_dir))])

    fig = plt.figure()
    feat_importance = pd.Series(model.feature_importances_, index=X.columns)
    #feat_importance.nlargest(5).plot(kind='barh')
    feat_importance.nlargest(8).plot(kind='barh')
    fig.savefig('{}/feat_importance.png'.format(graphs_dir_path))
    logging.info(" # "*20 + " feature_importance graph created")

    #-------------------------------------------------------------------------------
    # SNS_PAIRPLOT
    #-------------------------------------------------------------------------------
    fig = plt.figure()
    sns.pairplot(df)
    fig.savefig('{}/sns_pairplot.png'.format(graphs_dir_path))
    logging.info(" # "*20 + " SNS_PAIRPLOT GRAPH created")

    #-------------------------------------------------------------------------------
    # SNS HEAT_MAP 
    #-------------------------------------------------------------------------------
    fig = plt.figure()
    corr_mat = df.corr()
    top_corr_features = corr_mat.index
    plt.figure(figsize=(20,20))
    g = sns.heatmap(df[top_corr_features].corr(), annot=True, cmap="YlGnBu")
    fig.savefig('{}/sns_heatmap.png'.format(graphs_dir_path))
    logging.info(" # "*20 + " SNS HEAT_MAP  GRAPH created")

    #-------------------------------------------------------------------------------
    # SNS_DISTPLOT
    #-------------------------------------------------------------------------------
    
    fig = plt.figure()
    sns.distplot(y)
    fig.savefig('{}/SNS_DISTPLOT(Y).png'.format(graphs_dir_path))
    logging.info(" # "*20 + "SNS_DISTPLOT(Y).png   created")

    #return df 
    #-------------------------------------------------------------------------------
    # SAVING THE DATA TO real_data_combined_file_path
    #-------------------------------------------------------------------------------
    logging.info("----"*30)
    new_df = df = pd.concat((X, y), axis=1)
    
    save_local_df(new_df, cleaned_real_data_file_path)
    logging.info(" cleaned_real_data_file_path = {}".format(cleaned_real_data_file_path))
    #logging.info("----"*30)


             




if __name__=="__main__":

    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config/config.yaml")
    parsed_args = args.parse_args()
    config_path=parsed_args.config
    
    try:
        logging.info("starting StGE 02 EDA DATA")
        eda(config_path=parsed_args.config)
        logging.info("Stage 02 completed successfully and all the data is saved in the locals")
    except Exception as e:
        logging.info(e)
        raise e