FROM ubuntu:latest
MAINTAINER Aghasi Gevorgyan
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN mkdir /app
RUN chmod 777 /app
COPY app/requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY app/mq.py /app
RUN chmod +x /app/mq.py
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["mq.py"]
