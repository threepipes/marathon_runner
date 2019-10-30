DB=$1

touch $DB
echo "create table worker(id, label, num, result, create_datetime);" | sqlite3 $DB
