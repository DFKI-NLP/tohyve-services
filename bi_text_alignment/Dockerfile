FROM python:3.9.15

EXPOSE 8008

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ADD requirements.txt .
RUN python3 -m pip install -r requirements.txt
RUN python3 -m unidic download

WORKDIR /app
ADD . /app

CMD ["python3", "-m", "main"]