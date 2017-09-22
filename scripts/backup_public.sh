mysqldump -h$STOCKY_MYSQL_HOST -u$STOCKY_MYSQL_USER -p$STOCKY_MYSQL_PASS $STOCKY_MYSQL_NAME companies companies_meta quotes > /data/backups/stocky_$(date +"%Y_%m_%d").sql
