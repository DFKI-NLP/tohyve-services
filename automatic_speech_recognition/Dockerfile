FROM ubuntu:latest

EXPOSE 8000

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TRANSFORMERS_CACHE=/path/to/transformers

# RUN pip install --upgrade pip
# RUN apk add git
User root
RUN apt update
RUN apt-get install -y git
RUN apt install -y python3-pip
RUN apt install -y ffmpeg
# RUN apt-get install -y python3.9-tk

ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt
# RUN python3 -m pip install setuptools-rust


WORKDIR /app
ADD . /app

CMD ["python3", "-m", "main"]