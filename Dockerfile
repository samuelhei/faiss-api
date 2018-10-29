FROM ubuntu:16.04

MAINTAINER Samuel Heinrichs "ti.samuelh@gmail.com"

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get install -y wget zip

RUN cd /tmp \
    && wget https://github.com/samuelhei/mkl-so-files/archive/master.zip \
    && unzip master.zip \
    && mv /tmp/mkl-so-files-master/* /usr/local/lib \
    && rm master.zip

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]
 
CMD [ "application.py" ]