#!/bin/bash -e

temp_pw_file=$(mktemp)
master_password=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c16)

temp_user_config="/tmp/user_config.sql"

echo "CREATE DATABASE ${master_username}" >> $temp_user_config
echo "CREATE USER ${master_username} WITH ENCRYPTED PASSWORD '${master_password}'" >> $temp_user_config
echo "GRANT ALL PRIVILEGES ON DATABASE ${master_username} TO ${master_username};">> $temp_user_config
echo "ALTER USER ${master_username} WITH SUPERUSER;" >> $temp_user_config

sudo postgresql-setup initdb
sudo -u postgres psql -f $temp_user_config

rm -f ${temp_user_config}

ctx instance runtime-properties master_username ${master_username}
ctx instance runtime-properties master_password ${master_password}
