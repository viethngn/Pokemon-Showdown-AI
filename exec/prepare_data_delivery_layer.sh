#!/bin/sh

# exit when any command fails
set -e

# get the program dir
prog_dir=$(pwd)

mysql_host="localhost"
mysql_user="autoaccess"
mysql_password="autoaccess"
mysql_db="pokemon_showdown"

# Create data mart stored procedures
/usr/local/mysql/bin/mysql -h "$mysql_host" -u "$mysql_user" -p"$mysql_password" "$mysql_db" < "$prog_dir"/sql/ps_data_mart_stored_procedures.sql

# Create data mart mysql views
/usr/local/mysql/bin/mysql -h "$mysql_host" -u "$mysql_user" -p"$mysql_password" "$mysql_db" < "$prog_dir"/sql/ps_data_marts.sql

# data check sum test
echo "Start data check sum test"
python ps_check_sum_test.py

# Set up event scheduler to refresh views
/usr/local/mysql/bin/mysql -h "$mysql_host" -u "$mysql_user" -p"$mysql_password" "$mysql_db" < "$prog_dir"/sql/db_event_control.sql