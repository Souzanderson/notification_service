# Base Image
FROM python:3.8-alpine3.13

# Install netcat
# RUN apt-get update && \
#     apt-get -y install netcat && \
#     apt-get clean

# set working directory
WORKDIR /usr/src/app

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . /usr/src/app
EXPOSE 5590

# run server
CMD python app.py
