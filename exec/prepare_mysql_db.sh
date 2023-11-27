#!/bin/sh

# exit when any command fails
set -e

# get the program dir
prog_dir=$(pwd)

mysql_host="localhost"
mysql_user="autoaccess"
mysql_password="autoaccess"
mysql_db="pokemon_showdown"

# Run DDL script
/usr/local/mysql/bin/mysql -h "$mysql_host" -u "$mysql_user" -p"$mysql_password" < "$prog_dir"/sql/pokemon_showdown_DDL.sql

# Set DB procedures
/usr/local/mysql/bin/mysql -h "$mysql_host" -u "$mysql_user" -p"$mysql_password" "$mysql_db" < "$prog_dir"/sql/ps_data_warehouse_stored_procedures.sql

# Set trigger for Data Analytical Layer
/usr/local/mysql/bin/mysql -h "$mysql_host" -u "$mysql_user" -p"$mysql_password" "$mysql_db" < "$prog_dir"/sql/db_trigger_control.sql