FROM nvidia/cuda:12.2.0-base-ubuntu20.04
# FROM nvidia/cuda:11.6.2-base-ubuntu20.04

EXPOSE 8003

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TRANSFORMERS_CACHE=/path/to/transformers
ENV DEBIAN_FRONTEND=noninteractive

USER root
RUN apt update
RUN apt-get install -y git
RUN apt install -y python3-pip

ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt

RUN apt-get update && apt-get install -y libsndfile1 ffmpeg
RUN python3 -m pip install Cython
RUN python3 -m pip install nemo_toolkit['all']

# RUN apt install -y ffmpeg
# RUN apt-get install -y python3.9-tk


# RUN python3 -m pip install nemo_toolkit['all']
# RUN python3 -m pip install setuptools-rust

# Create a directory to store model files inside the container
RUN mkdir -p /app/models
RUN mkdir -p /app/created_audio
WORKDIR /app

# Copy model files and dependencies into the container
COPY models/ /app/models/

# Add all necessary scripts
ADD main.py /app
ADD model.py /app
ADD convert.py /app

# ADD . /app

CMD ["python3", "-m", "main"]