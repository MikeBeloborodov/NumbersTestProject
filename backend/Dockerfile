FROM python:alpine
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN apk update
RUN apk upgrade
RUN apk add bash
COPY . .