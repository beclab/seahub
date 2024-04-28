#!/bin/bash
#
#
#

# 设置数据库连接参数
#DB_HOST="localhost"
#DB_PORT="5432"
#DB_NAME1="ccnet"
#DB_NAME2="seafile"
#DB_NAME3="seahub"
#DB_USER="postgres"

#DB_PASSWORD="123456"
echo "DB_HOST= $DB_HOST"
echo "DB_PORT= $DB_PORT"
echo "DB_NAME1= $DB_NAME1"
echo "DB_NAME2= $DB_NAME2"
echo "DB_NAME3= $DB_NAME3"
echo "DB_USER= $DB_USER"
echo "DB_PASSWORD= $DB_PASSWORD"

# 设置 SQL 文件路径
SQL_FILE1="init_pgdata/ccnet.sql"
SQL_FILE2="init_pgdata/seafile.sql"
SQL_FILE3="init_pgdata/seahub.sql"

# 设置 PGPASSWORD 环境变量
export PGPASSWORD="$DB_PASSWORD"

# 设置要检查的表名
TABLE_NAME1="Group"
TABLE_NAME2="branch"
TABLE_NAME3="abuse_reports_abusereport"

# 使用 PSQL 查询数据库是否存在
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME1"
if [ $? -eq 0 ]; then
    echo "数据库 $DB_NAME1 存在"
else
    echo "数据库 $DB_NAME1 不存在"
##    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME1"
#    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME1 -f $SQL_FILE1
#    echo "初始化完成"
fi

psql -h $DB_HOST -p $DB_PORT -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME2"
if [ $? -eq 0 ]; then
    echo "数据库 $DB_NAME1 存在"
else
    echo "数据库 $DB_NAME1 不存在"
fi

psql -h $DB_HOST -p $DB_PORT -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME3"
if [ $? -eq 0 ]; then
    echo "数据库 $DB_NAME1 存在"
else
    echo "数据库 $DB_NAME1 不存在"
fi

# 使用 PSQL 查询表是否存在
#psql -h $DB_HOST -p $DB_PORT -d $DB_NAME1 -U $DB_USER -c "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '$TABLE_NAME1');" | grep -q 't'
#if [ $? -eq 0 ]; then
#    echo "数据库 $DB_NAME1 存在"
#else
#    echo "数据库 $DB_NAME1 不存在，正在初始化..."
##    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME1"
#    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME1 -f $SQL_FILE1
#    echo "初始化完成"
#fi
#
#psql -h $DB_HOST -p $DB_PORT -d $DB_NAME2 -U $DB_USER -c "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '$TABLE_NAME2');" | grep -q 't'
#if [ $? -eq 0 ]; then
#    echo "数据库 $DB_NAME2 存在"
#else
#    echo "数据库 $DB_NAME2 不存在，正在初始化..."
##    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME2"
#    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME2 -f $SQL_FILE2
#    echo "初始化完成"
#fi
#
#psql -h $DB_HOST -p $DB_PORT -d $DB_NAME3 -U $DB_USER -c "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '$TABLE_NAME3');" | grep -q 't'
#if [ $? -eq 0 ]; then
#    echo "数据库 $DB_NAME3 存在"
#else
#    echo "数据库 $DB_NAME3 不存在，正在初始化..."
##    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME3"
#    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME3 -f $SQL_FILE3
#    echo "初始化完成"
#fi

# 使用 PSQL 查询数据库是否存在
#psql -h $DB_HOST -p $DB_PORT -U $DB_USER -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME1"
#if [ $? -eq 0 ]; then
#    echo "数据库 $DB_NAME1 存在"
#else
#    echo "数据库 $DB_NAME1 不存在，正在初始化..."
##    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME1"
#    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME1 -f $SQL_FILE1
#    echo "初始化完成"
#fi

# 清除 PGPASSWORD 环境变量（可选）
unset PGPASSWORD

seaf-server -c ~/dev/conf -d ~/dev/seafile-data -D all -f -l - &
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
