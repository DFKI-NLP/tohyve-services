FROM nvidia/cuda:12.2.0-base-ubuntu20.04

EXPOSE 8001

#set up environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TRANSFORMERS_CACHE=/path/to/transformers
ENV DEBIAN_FRONTEND=noninteractive

USER root
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python3-pip
RUN apt-get install -y ffmpeg

ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt

WORKDIR /app
ADD . /app

CMD ["python3", "-m", "main"]