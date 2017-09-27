mkdir /home/alix/backup/stocky
dblocaldump stocks2 companies companies_meta quotes > /home/alix/backup/stocky/stocky_now.sql
dblocaldump -d stocks2 portfolios portfolios_events users users_meta >> /home/alix/backup/stocky/stocky_now.sql
cd /home/alix/backup/stocky/
zip -r /home/alix/backup/stocky/stocky.zip ./*
docker cp stocky.zip stocky:/opt/stocky/app/static/data/stocky_data.zip
rm -rf /home/alix/backup/stocky