FROM ubuntu:18.04

ENV FLASK_APP main.py
ENV FLASK_CONFIG production

RUN adduser flasky
WORKDIR /home/flasky

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y gcc python3-dev curl libcairo2-dev

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install -r requirements.txt

USER flasky

COPY app app
COPY main.py README.md config.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
