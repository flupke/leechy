MANAGE=`pwd`/manage.py

$MANAGE makemessages -a -e .html -e .txt
$MANAGE compilemessages
cd ../src/leechy
$MANAGE makemessages -a -e .html -e .txt
$MANAGE compilemessages
