FROM python:3.11-slim
MAINTAINER Pasit Yodsoi
LABEL Dev="Pasit Y."

RUN apt-get update -y && apt-get install -y vim
COPY ./package.txt /package.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /package.txt
RUN rm -f /package.txt

WORKDIR /app
COPY ./src/main.py .

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug" ]