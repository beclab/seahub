#!/bin/bash

echo "DB_HOST= $DB_HOST"
echo "DB_PORT= $DB_PORT"
echo "DB_NAME1= $DB_NAME1"
echo "DB_NAME2= $DB_NAME2"
echo "DB_NAME3= $DB_NAME3"
echo "DB_USER= $DB_USER"
echo "DB_PASSWORD= $DB_PASSWORD"

SQL_FILE1="init_pgdata/ccnet.sql"
SQL_FILE2="init_pgdata/seafile.sql"
SQL_FILE3="init_pgdata/seahub.sql"

export PGPASSWORD="$DB_PASSWORD"

TABLE_NAME1="Group"
TABLE_NAME2="branch"
TABLE_NAME3="abuse_reports_abusereport"

psql -h $DB_HOST -p $DB_PORT -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME1"
if [ $? -eq 0 ]; then
    echo "database $DB_NAME1 exists"
else
    echo "database $DB_NAME1 doesn't exist"
fi

psql -h $DB_HOST -p $DB_PORT -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME2"
if [ $? -eq 0 ]; then
    echo "database $DB_NAME1 exists"
else
    echo "database $DB_NAME1 doesn't exist"
fi

psql -h $DB_HOST -p $DB_PORT -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME3"
if [ $? -eq 0 ]; then
    echo "database $DB_NAME1 exists"
else
    echo "database $DB_NAME1 doesn't exist"
fi

unset PGPASSWORD

seaf-server -c ~/dev/conf -d ~/dev/seafile-data -D all -f -l -
