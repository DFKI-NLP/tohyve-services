FROM huggingface/transformers-pytorch-gpu:4.29.2

EXPOSE 8000

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV TRANSFORMERS_CACHE=/path/to/transformers

USER root
RUN apt update
RUN apt-get install -y git
RUN apt install -y python3-pip
RUN apt install -y ffmpeg

ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt


WORKDIR /app
ADD . /app

CMD ["python3", "-m", "main"]