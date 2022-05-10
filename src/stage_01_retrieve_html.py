# importing necessary modules
import requests
from io import BytesIO
import zipfile
import os
import time 
import argparse
import requests
import sys
from src.utils.all_utils import create_directory, read_yaml

def retrieve_html(config_path):

    config = read_yaml(config_path)

    site_name = config["Data"]['site_name']
    #city_code = config["Data"]['city_code']

    artifacts_dir = config["artifacts"]['artifacts_dir']
    data_local_dir = config["artifacts"]['data_local_dir']
    raw_data_dir = config["artifacts"]['raw_data_dir']
    #html_data_dir = config["artifacts"]['html_data_dir']

    data_local_dir_path = os.path.join(artifacts_dir, data_local_dir)

    create_directory(dirs= [data_local_dir_path])

    dementia_local_dir_path = os.path.join(data_local_dir_path, raw_data_dir)

    #print("#"*20 + " dementia_local_dir_path " + "#"*20)
    #print(dementia_local_dir_path)
    #print("#"*20 + " dementia_local_dir_path " + "#"*20)
   
    
    #we are going to fetch dta from the site
    print('Downloading started')
    
    # Downloading the file by sending the request to the URL
    req = requests.get(site_name)
    print('Downloading Completed')

    # extracting the zip file contents
    zip_file= zipfile.ZipFile(BytesIO(req.content))
    print("##"*10 +"  location of downloaded unzipped file {} \n" .format( dementia_local_dir_path))
    zip_file.extractall(dementia_local_dir_path)
    
    
    
if __name__=="__main__":

    args = argparse.ArgumentParser()

    args.add_argument("--config", "-c", default="config/config.yaml")

    parsed_args = args.parse_args()

    start_time=time.time()

    retrieve_html(config_path=parsed_args.config)

    stop_time=time.time()
    print("time taken{}".format(stop_time-start_time))
 
 