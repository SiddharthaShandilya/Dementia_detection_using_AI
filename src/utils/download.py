"""

from __future__ import print_function
import requests
from io import BytesIO
import zipfile
import os
from src.utils.all_utils import create_directory, read_yaml
import logging
import time

##############################################################


import io

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


def download_file(real_file_id):
    '''Downloads a file
    Args:
        real_file_id: ID of the file to download
    Returns : IO object with location.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    '''
    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build('drive', 'v3', credentials=creds)

        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.getvalue()


if __name__ == '__main__':
    download_file(real_file_id='11on8iRLolH6uPQ4KDwn7a-WdguOtnNR8')

"""
############################################################################
"""
def remote_data_download(config_path, site_name):
    '''
    remote_data_download allows user to load the given remote dataset rpository in the desired local directory
    
    Parameters
    ----------
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

    dementia_local_dir_path = os.path.join(data_local_dir_path)

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

"""