FROM apache/spark:3.5.0

USER root

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER spark

WORKDIR /opt/spark/jars

COPY jar_urls.txt .

RUN wget -i jar_urls.txt -q

RUN rm -f jar_urls.txt

WORKDIR /opt/spark