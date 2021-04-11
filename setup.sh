#!/bin/sh

DBuser=$1
PASSWDDB=$2
# store them in a config which will use also the app
echo "USERNAME=${DBuser}\nPASSWORD=${PASSWDDB}" > DB_CONFIG

# setup all DBs
mysql -u root<<MYSQL_SCRIPT
CREATE USER if not exists ${DBuser}@'%' IDENTIFIED BY '${PASSWDDB}';

CREATE DATABASE if not exists SimpleTabs;
GRANT ALL PRIVILEGES ON SimpleTabs.* TO ${DBuser}@'%';
FLUSH PRIVILEGES;
MYSQL_SCRIPT