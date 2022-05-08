import os
import time 
import argparse
import requests
import sys
from src.utils.all_utils import create_directory, read_yaml

def retrieve_html(config_path):

    config = read_yaml(config_path)

    site_name = config["Data"]['site_name']
    city_code = config["Data"]['city_code']

    artifacts_dir = config["artifacts"]['artifacts_dir']
    data_local_dir = config["artifacts"]['data_local_dir']
    html_data_dir = config["artifacts"]['html_data_dir']

    data_local_dir_path = os.path.join(artifacts_dir, data_local_dir)

    create_directory(dirs= [data_local_dir_path])

    html_local_dir_path = os.path.join(data_local_dir_path, html_data_dir)

    print("#"*20 + " html_directory file path " + "#"*20)
    print(html_local_dir_path)
    print("#"*20 + " html_directory file path " + "#"*20)
   
    
    #we are going to fetch every month's data from year 2103 to 2020
    for year in range(2013,2019):
        for month in range(1,13):
            
            if month<10:
                url="{}/0{}-{}/{}".format(site_name, month, year,city_code)
                
            else:
                 url="{}/{}-{}/{}".format(site_name, month, year,city_code)
                 
            text = requests.get(url)
            text_utf = text.text.encode('utf-8')
        
            if not os.path.exists("{}/{}".format(html_local_dir_path,year)):
                                       
                os.makedirs("{}/{}".format(html_local_dir_path,year))
                
            with open("{}/{}/{}.html".format(html_local_dir_path,year,month),"wb") as output:
                
                output.write(text_utf)

            print("{}/ {} / {} created".format(html_local_dir_path, year, month))
                  
    sys.stdout.flush()
    
if __name__=="__main__":

    args = argparse.ArgumentParser()

    args.add_argument("--config", "-c", default="config/config.yaml")

    parsed_args = args.parse_args()

    start_time=time.time()

    retrieve_html(config_path=parsed_args.config)

    stop_time=time.time()
    print("time taken{}".format(stop_time-start_time))