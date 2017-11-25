FROM ubuntu:latest
MAINTAINER Aghasi Gevorgyan
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN mkdir -p /app/templates
RUN chmod -R 777 /app
COPY app/getlog.py /app
COPY app/requirements.txt /app
COPY templates/form.html /app/templates
RUN chmod +x /app/getlog.py
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["getlog.py"]
