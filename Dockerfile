FROM ubuntu
RUN apt-get update --fix-missing
RUN apt-get install git -y
RUN apt-get install python3-pip -y
#RUN python -m pip install --upgrade pip
RUN git clone https://github.com/SiddharthaShandilya/air_quality_index_prediction.git
EXPOSE 5000
COPY dvc.yaml /air_quality_index_prediction
WORKDIR /air_quality_index_prediction
RUN pip install -r requirements.txt
RUN dvc dag | cat > dvc_dag_image.txt
#RUN echo " dvc repro" > air_quality_index_prediction/dvc.sh
RUN cat dvc_dag_image.txt
RUN dvc repro dvc.yaml