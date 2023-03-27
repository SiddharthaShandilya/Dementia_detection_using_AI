 ![](https://socialify.git.ci/SiddharthaShandilya/Dementia_detection_using_AI/image?description=1&font=Inter&forks=1&issues=1&language=1&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Dark)



[![forthebadge](https://forthebadge.com/images/badges/built-by-developers.svg)](http://forthebadge.com)   [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)      [![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)

<!--
[![Gem Version](https://badge.fury.io/rb/colorls.svg)](https://badge.fury.io/rb/colorls)
[![CI](https://github.com/athityakumar/colorls/actions/workflows/ruby.yml/badge.svg)](https://github.com/athityakumar/colorls/actions/workflows/ruby.yml)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields)](http://makeapullrequest.com)
-->
This is a machine learning project that predicts whether a person is demented or not based on their brain MRI scans and other relevant information.



# Table of contents

- [Project Overview](#project-overview)
- [Installation](#installation)
- [Recommended configurations](#recommended-configurations)
- [Custom configurations](#custom-configurations)
- [Updating](#updating)
- [Output](#output)
- [Uninstallation](#uninstallation)
- [Future Work](#future-work)
- [References](#references)


# Project Overview

[(Back to top)](#table-of-contents)

Dementia is a progressive neurological disorder that affects millions of people worldwide. Early detection and diagnosis of dementia can significantly improve patient outcomes and quality of life. In this project, we have developed a machine learning model that predicts whether a person is demented or not based on their brain MRI scans and other relevant information.

Our model uses XGBoost, a popular machine learning algorithm, to train on a dataset of MRI scans and demographic information from patients with and without dementia. The model achieves an accuracy of 95% on the test set and has the potential to be a valuable tool for early detection and diagnosis of dementia.


# Installation


[(Back to top)](#table-of-contents)

1. Install git (preferably, version >= 2.0) and python (preferably, version >=3.6)
 [(windows)](https://www.maketecheasier.com/install-git-bash-on-windows/)
 For Linux :
 ```bash
    sudo yum instal git -y
    sudo yum install python -y
 ```
 
2. Copy the github url from the repository : 

 ```bash
 https://github.com/SiddharthaShandilya/Dementia_detection_using_AI.git
 ```

3. Select a Directory in local system and use 

  ```bash 
  git clone https://github.com/SiddharthaShandilya/Dementia_detection_using_AI.git          
  ```

    *Note for `git clone command`  Please make sure that you have proper internet connection. *

    *Note for `python` Please try to anaconda for running the app.*  

4. Create a seperate virtual environment to avoid conflict between python libraries :
```bash
    python3 -m venv new-env 
```
In case for anaconda we can use below commands
```bash
    conda create --prefix ./env
    conda activate ./env
```

5. In case tou want to Activate the virtual env follow the given instructions: 👉 [(click Here)](https://www.programshelp.com/help/python/activate_virtual_environment_python_windows_10.html)

6. Install all the libraries for the application.
```bash
pip3 install -r requirements.txt
```
7. Once the environment is created use following commands to start
```bash
git init
dvc init
dvc dag
dvc repro
```

6. Have a look at [Recommended configurations](#recommended-configurations) and [Custom configurations](#custom-configurations).


</br></br>


# Custom configurations

[(Back to top)](#table-of-contents)

1. In the project we are running flask application by using python3  which might not work so try below mentioned commands:
    ```sh
    python/python3 app.py
    ```
    or
    ```sh
    flask run 
    ```

</br></br>



# Recommended configurations

[(Back to top)](#table-of-contents)


You can overwrite the existing code according to your needs and changing them.

- Note :

1. Please have a look at the dvc.yaml file , Here i have used python3.7 version so if your console takes python3 to run python make sure to change all the commands in dvc.yaml file.

<br>

2. If any change regarding the file are concerned you are advised to change the config file in location ' /config/config.yaml '. For eg.. the location of dataset in thsi code is of a lcoal storage ../dementia_dataset, this might not be in you case so change the code accordingly.

 

# Updating

[(Back to top)](#table-of-contents)

Want to update to the latest version of `dementia_detection`? make the required change and give us a pull request
 
```sh
git push https://github.com/SiddharthaShandilya/Dementia_detection_using_AI.git
```



</br></br>

# Output
[(Back to top)](#table-of-contents)

For Downloading Docker Image
```sh
docker pull centos104/dementia_detection_web_app
```

Below is some screenshot of the web application when it is successfully launched.


![web_UI](https://github.com/SiddharthaShandilya/Dementia_detection_using_AI/blob/master/screen_shots/test_web1_front.png)
![web_UI_backend_output](https://github.com/SiddharthaShandilya/Dementia_detection_using_AI/blob/master/screen_shots/test_web1_back.png)


<br></br>

# Uninstallation

[(Back to top)](#table-of-contents)

Want to uninstall ? No issues (sob). Please feel free to open an issue regarding how we can enhance `dementia_detection app`.


```sh
ctrl + A, ctrl + shift + delete
```

# Future Work
[(Back to top)](#table-of-contents)

In the future, we plan to improve the accuracy of the model by using a larger dataset and exploring more advanced machine learning techniques. Additionally, we plan to deploy the model as a web application to make it more accessible to healthcare professionals and patients.


# References
[(Back to top)](#References)

Dataset: https://www.kaggle.com/tourist55/alzheimers-dataset-4-class-of-images

XGBoost: https://xgboost.readthedocs.io/en/latest/index.html
