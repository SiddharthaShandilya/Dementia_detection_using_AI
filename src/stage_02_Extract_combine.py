import pandas as pd
import matplotlib.pyplot as plt
import os, argparse
import csv
#from stage_02_aqt_data_processing import avg_data
from src.utils.all_utils import avg_data, read_yaml
import requests
import sys 
from bs4 import BeautifulSoup


#_____________________________________________________________________________
#
#          Extracting Data From Beautiful Soup
#_____________________________________________________________________________


def met_data(html_local_dir_path,month, year):
    print(" html_local_dir_path = {}".format(html_local_dir_path))
    file_html=open('{}/{}/{}.html'.format(html_local_dir_path,year,month),'rb')
    plain_text = file_html.read()

    #print("-"*10 + " META_DATA" + "-"*10)
    tempd=[]
    finald=[]
    
    soup = BeautifulSoup(plain_text,'html.parser')
    
    for table in soup.findAll("table",{"class":"medias mensuales numspan"}):
        for tbody in table:
            for tr in tbody:
                a = tr.get_text()
                tempd.append(a)
                
                
    #print(type(tempd))
                
    rows = len(tempd)/15
  
    for times in range(round(rows)):
        newtempd=[]
        for i in range(15):
            newtempd.append(tempd[0])
            tempd.pop(0)
            
        finald.append(newtempd)
        #print(finald)
        
    length = len(finald)
    print(" length of final d = {}  month = {}  year = {}".format(length,month, year))

        
    finald.pop(length-1)  # removing the last row which contains mean and mode

    finald.pop(0)  # removing the first row which contains all the columns name
    
    
    # removing the columns with null values
    for a in range (len(finald)):
        
        finald[a].pop(6) # now that we have poped 6th first so the entire column alignment needs to be changed accordingly
        finald[a].pop(13)# 15th columns
        finald[a].pop(12) # 14th column
        finald[a].pop(11) # 13th column
        finald[a].pop(10) # 12th column
        finald[a].pop(9) # 11th column
        finald[a].pop(0) # removing column 1st because removing 6th column does not affect 0th position
    
    #print(finald)    
    return finald




#_____________________________________________________________________________
#
#           Combining data
#_____________________________________________________________________________

def data_combine(real_data_dir_path,year, cs):
    
    for a in pd.read_csv(str(real_data_dir_path)+'/real_'+str(year)+'.csv',chunksize=cs):
        
        print(str(real_data_dir_path)+'/real_'+str(year)+'.csv')

        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
        
    return mylist

#_____________________________________________________________________________
#
#           Main Function
#_____________________________________________________________________________


if __name__ == "__main__":

    args = argparse.ArgumentParser()

    args.add_argument("--config", "-c", default="config/config.yaml")

    parsed_args = args.parse_args()

    config_path=parsed_args.config

    config = read_yaml(config_path)
    

    artifacts_dir = config["artifacts"]['artifacts_dir'] # points to artifacts folder
    data_local_dir = config["artifacts"]['data_local_dir'] # points to data folder inside artifacts
    html_data_dir = config["artifacts"]['html_data_dir'] # points to Html_Data folder inside artifacts/data
    aqi_data_dir = config["artifacts"]['aqi_data_dir'] # points to AQI folder inside artifacts/data
    real_data_dir = config["artifacts"]['real_data_dir'] # points to Real-Data folder inside artifacts/data
    real_data_combined_file = config["artifacts"]['real_data_combined_file'] # points to  Real_Combine.csv file inside artifacts/data/Real-Data

    data_local_dir_path = os.path.join(artifacts_dir, data_local_dir)
    html_local_dir_path = os.path.join(data_local_dir_path, html_data_dir)
    aqi_data_dir_path = os.path.join(data_local_dir_path, aqi_data_dir)
    real_data_dir_path = os.path.join(data_local_dir_path, real_data_dir)

    real_data_combined_file_path = os.path.join(real_data_dir_path, real_data_combined_file)

    print("#"*20 + " html_directory file path " + "#"*20)
    print(" html_local_dir_path = {}".format(html_local_dir_path))
    print(" haqi_data_dir_path = {}".format(aqi_data_dir_path))
    print(" real_data_dir_path = {}".format(real_data_dir_path))
    print(" real_data_combined_file_path = {}".format(real_data_combined_file_path))
    print("#"*20 + " html_directory file path " + "#"*20)
    
    if not os.path.exists('{}/'.format(real_data_dir_path)):
        os.makedirs('{}/'.format(real_data_dir_path))
    for year in range(2013, 2019):
        final_data=[]
        with open(str(real_data_dir_path)+'/real_'+ str(year) + '.csv','w') as csvfile:
            wr = csv.writer(csvfile, dialect='excel')
            wr.writerow(
                ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])   
        
        for month in range(1,13):
            temp = met_data(html_local_dir_path,month, year)         
            final_data = final_data + temp
        
        pm = avg_data(aqi_data_dir_path, year)

        if len(pm) == '364':
            pm.insert(364,'_')

        for i in range (len(final_data)-1):
            final_data[i].insert(8,pm[i])


            
        with open(str(real_data_dir_path)+'/real_{}.csv'.format(year), 'a') as csvfile:

            wr = csv.writer(csvfile, dialect='excel')
            for row in final_data:
                flag = 0
                for elem in row:
                    if elem == "" or elem == "-":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)
                   

    data_2013 = data_combine(real_data_dir_path,2013, 600)
    data_2014 = data_combine(real_data_dir_path,2014, 600)
    data_2015 = data_combine(real_data_dir_path,2015, 600)
    data_2016 = data_combine(real_data_dir_path,2016, 600)
    #data_2017 = data_combine(2017, 600)
    #data_2018 = data_combine(2018, 600)
     
    total=data_2013+data_2014+data_2015+data_2016 #+data_2017+data_2018
    
    

    with open('{}'.format(real_data_combined_file_path), 'w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)
        


df=pd.read_csv('{}'.format(real_data_combined_file_path))
print(df.head())



