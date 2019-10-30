DB=$1

touch $DB
# TODO: read scheme from settings
echo "create table worker(id, label, num, result, create_datetime);" | sqlite3 $DB
