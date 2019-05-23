FROM alpine
RUN apk update
RUN apk add python3

ADD requirements.txt requirements.txt
RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r requirements.txt



