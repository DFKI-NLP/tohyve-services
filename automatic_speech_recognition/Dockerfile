FROM nvidia/cuda:12.2.0-base-ubuntu20.04
# FROM nvidia/cuda:11.6.2-base-ubuntu20.04

EXPOSE 8001

#set up environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TRANSFORMERS_CACHE=/path/to/transformers
ENV DEBIAN_FRONTEND=noninteractive

USER root
RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install -y git
RUN apt-get install -y ffmpeg

ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt

# Create a directory to store model files inside the container
RUN mkdir -p /app/models
WORKDIR /app

# Copy model files and dependencies into the container
COPY models/ /app/models/

# Add all necessary scripts
ADD main.py /app
ADD model.py /app
ADD transcribe.py /app

CMD ["python3", "-m", "main"]