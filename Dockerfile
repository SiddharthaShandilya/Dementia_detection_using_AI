FROM python:3.7-buster
RUN apt-get install git -y
#RUN apt-get install python3-pip -y
RUN mkdir opt/dementia_detection 
WORKDIR opt/
RUN python -m pip install --upgrade pip && git clone https://github.com/SiddharthaShandilya/Dementia_detection_using_AI.git
WORKDIR opt/Dementia_detection_using_AI
EXPOSE 5000:5000
COPY . .
RUN pip install -r requirements.txt


CMD [ "python", "app.py" ]


