cd ~/COMPOSE
docker-compose -f lab1.yml up -d
cd /home/q/PY3
source bin/activate
echo "Creating MariaDb database and table and insert 10^N records"
time python lab1_createMariaDb.py
echo ""
echo "-------------------------------------------------------------"
echo ""
echo "Migrating table from MariaDb to MongoDb"
time python lab1.py
echo ""
echo "-------------------------------------------------------------"
echo ""
echo "Testing VERY BAD algoritm"
time python lab1_algorithm.py
deactivate
cd ..
