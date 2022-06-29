from src.utils.all_utils import read_yaml, create_directory
import argparse, os, shutil
import pandas as pd
from tqdm import tqdm
import logging


#-------------------------------------------------------------------------------
#   Creating a looging with timestamp and regex 
#-------------------------------------------------------------------------------

logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'stage_01_running_logs.log'), level=logging.INFO, format=logging_str,filemode="a")

#-------------------------------------------------------------------------------
#   copy_file
#-------------------------------------------------------------------------------

def copy_file(source_download_dir, data_local_dir_path): 
    list_of_files = os.listdir(source_download_dir)
    N = len(list_of_files)
    logging.info(f"\n\n location of lacal{ data_local_dir_path}")

    for file in tqdm(list_of_files, total=N, desc= "copying file from {} to {}".format(source_download_dir, data_local_dir_path), colour="green"):
        src = os.path.join(source_download_dir, file)
        dest = os.path.join(data_local_dir_path, file)
        shutil.copy(src, dest)

#-------------------------------------------------------------------------------
#   get_data
#-------------------------------------------------------------------------------

def get_data(config_path):

    config = read_yaml(config_path)
    source_download_dirs = config["Data"]["local_source_download_path"]
    artifacts_dir = config["artifacts"]['artifacts_dir']
    data_local_dir = config["artifacts"]['data_local_dir']
    raw_data_dir = config["artifacts"]['raw_data_dir']

    #html_data_dir = config["artifacts"]['html_data_dir']

    data_local_dir_path = os.path.join(artifacts_dir, data_local_dir, raw_data_dir )

    #for source_download_dir, data_local_dir_path in tqdm(zip(source_download_dirs, data_local_dir_path), total=2, desc="list of folders", colour="red"):
    create_directory([data_local_dir_path])
    copy_file(source_download_dirs, data_local_dir_path)


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config","-c", default="config/config.yaml")
    parsed_args = args.parse_args()
    
    try:
        logging.info("starting StGE 01 LOADING DATA")
        get_data(config_path = parsed_args.config)
        logging.info("Stage 01 completed successfully and all the data is saved in the locals")
    except Exception as e:
        logging.info(e)
        raise e