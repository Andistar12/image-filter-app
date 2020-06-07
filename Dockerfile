FROM python:3
MAINTAINER Andy Nguyen "andyn@uoregon.edu"
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev build-essential
RUN pip install flask pillow
COPY . /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["app.py"]
