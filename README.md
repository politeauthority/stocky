# PoliteAuthority Stocks (pas)
Stock application to view and track portfolios. Currently up at https://politeauthority.me
note: because of a current issue getting the run.sh script to run via Dockers 'CMD' tool you have to run another command after the container is started.
This will be updated eventually


## Environmental Vars
ENV Var | Default | Description
--- | --- | --- 
STOCKY_MYSQL_HOST | MySQL Database Host | None
STOCKY_MYSQL_USER | MySQL Database User | None
STOCKY_MYSQL_PASS | MySQL Database Password | None
STOCKY_BUILD | Build type, set "LIVE" or "DEV"| DEV
PA_APP_DATA_PATH | (optional) Log space, temp space and other disk | /data/
TZ | The timezone for the container | America/Denver

## Docker Instructions
Build the docker container
```
docker build -t stocky .
```

Example development docker run script
```
docker stop stocky
docker rm stocky
docker run \
    --name=pas_dev \
    -e STOCKY_MYSQL_HOST="127.0.0.1" \
    -e STOCKY_MYSQL_USER="user" \
    -e STOCKY_MYSQL_PASS="password" \
    -e STOCKY_BUILD="DEV" \
    -v /Users/alix/pas/:/data/ \
    -v /Users/alix/repos/politeauthority/:/opt/politeauthority/ \
    -p 80:80 \
    -td \
    stocky:latest
```

Example live deployment
```
docker stop stocky
docker rm stocky
docker run \
    --name=pas \
    -d \
    -e STOCKY_MYSQL_HOST="127.0.0.1" \
    -e STOCKY_MYSQL_USER="user" \
    -e STOCKY_MYSQL_PASS="password" \
    -e STOCKY_BUILD="LIVE" \
    -e VIRTUAL_HOST=politeauthority.me \
    --restart=always \
    stocky
```

The Mysql Container runs like so,
```
docker stop some-mysql
docker rm some-mysql
docker run \
    --name=some-mysql \
    -e MYSQL_ROOT_PASSWORD=killer-root-pass \
    -v /home/me/data/mysqldata/:/var/lib/mysql \
    -d \
    -p 3306:3306 \
     mysql:latest
```