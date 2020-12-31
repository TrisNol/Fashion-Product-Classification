FROM tensorflow/tensorflow:latest-py3

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 libgl1-mesa-glx  -y

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .
EXPOSE 5000

CMD [ "python", "./app.py" ]