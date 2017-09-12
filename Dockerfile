FROM debian:jessie
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    git \
    python-pip \
    python \
    python-mysqldb

RUN mkdir /data/ && \
    cd /opt/ && \
    git clone https://github.com/politeauthority/stocky.git && \
    cd stocky && \
    pip install -r requirements.txt 

ENV STOCKY_MYSQL_HOST="Host"
ENV STOCKY_MYSQL_USER="User"
ENV STOCKY_MYSQL_PASS="Pass"
ENV STOCKY_MYSQL_PORT=3306
ENV STOCKY_MYSQL_NAME="stocky"
ENV PA_BASE_LOGGING_DIR='/data/logs'
ENV PA_BUILD="dev"
ENV PA_APP_DATA_PATH="/data/"
ENV TZ=America/Denver

VOLUME /opt/stocky/
VOLUME /data/

EXPOSE 80
