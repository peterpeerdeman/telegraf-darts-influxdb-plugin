FROM python:3.9.5-slim

RUN apt-get -y update  && apt-get install -y \
  python3-dev \
  apt-utils \
  python-dev \
  build-essential \
&& rm -rf /var/lib/apt/lists/*

RUN pip install darts
RUN pip install numpy
RUN pip install influxdb-client[ciso]
RUN pip install influx_line_protocol

WORKDIR /app

COPY . /app

CMD python app.py
