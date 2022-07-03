import requests
from io import BytesIO
import zipfile
import os
from src.utils.all_utils import create_directory, read_yaml
import logging
import time

def retrieve_html(config_path, site_name):
    '''
    retrieve_html allows user to load the given remote dataset rpository in the desired local directory
    INPUT : Config_path : location of the config.yaml file 
            site_name : name of the dataset remote repository
    OUTPUT : the dataset is stored in the local storage
    '''

    config = read_yaml(config_path)

    #city_code = config["Data"]['city_code']

    artifacts_dir = config["artifacts"]['artifacts_dir']
    data_local_dir = config["artifacts"]['data_local_dir']
    raw_data_dir = config["artifacts"]['raw_data_dir']
    #html_data_dir = config["artifacts"]['html_data_dir']

    data_local_dir_path = os.path.join(artifacts_dir, data_local_dir)

    create_directory(dirs= [data_local_dir_path])

    dementia_local_dir_path = os.path.join(data_local_dir_path, raw_data_dir)

    #logging.info("#"*20 + " dementia_local_dir_path " + "#"*20)
    #logging.info(dementia_local_dir_path)
    #logging.info("#"*20 + " dementia_local_dir_path " + "#"*20)
   
    
    #we are going to fetch dta from the site
    logging.info('Downloading started')
    
    # Downloading the file by sending the request to the URL
    req = requests.get(site_name)
    logging.info('Downloading Completed')

    # extracting the zip file contents
    zip_file= zipfile.ZipFile(BytesIO(req.content))
    logging.info("##"*10 +"  location of downloaded unzipped file {} \n" .format( dementia_local_dir_path))
    zip_file.extractall(dementia_local_dir_path)