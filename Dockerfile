FROM python:3.7-buster

RUN python -m pip install --upgrade pip

WORKDIR /opt/dementia_detection

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "app.py" ]
