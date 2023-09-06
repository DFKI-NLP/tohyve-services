# FROM nvidia/cuda:12.2.0-base-ubuntu20.04
FROM nvidia/cuda:11.6.2-base-ubuntu20.04

EXPOSE 8002

#set up environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TRANSFORMERS_CACHE=/path/to/transformers
ENV DEBIAN_FRONTEND=noninteractive
# ENV GIT_LFS_SKIP_SMUDGE=1

USER root
RUN apt update
RUN apt-get install -y git
RUN apt install -y python3-pip

ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt 

# Create a directory to store model files inside the container
RUN mkdir -p /app/models
RUN mkdir -p /app/images
WORKDIR /app

# Copy model files and dependencies into the container
COPY models/ /app/models/
COPY images/ /app/images/

# Add all necessary scripts
# ADD DFKI_ToHyVe_logo.jpg /app
ADD main.py /app
ADD model.py /app
ADD translator.py /app
ADD mt.py /app
# ADD  . /app

CMD ["python3", "-m", "main"]