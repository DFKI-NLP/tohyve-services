FROM ubuntu:latest

EXPOSE 8000

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TRANSFORMERS_CACHE=/path/to/transformers

# RUN pip install --upgrade pip
# RUN apk add git
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


WORKDIR /app
ADD . /app

CMD ["python3", "-m", "main"]