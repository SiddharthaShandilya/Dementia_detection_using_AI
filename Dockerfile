FROM python:3.7-buster

#RUN apt-get install git -y
#RUN apt-get install python3-pip -y
RUN python -m pip install --upgrade pip
#RUN git clone https://github.com/SiddharthaShandilya/air_quality_index_prediction.git
RUN mkdir opt/dementia_detection
WORKDIR opt/dementia_detection

COPY . .

EXPOSE 5000:5000

RUN pip install -r requirements.txt


CMD [ "python", "app.py" ]


