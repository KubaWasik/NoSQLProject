cd ~/COMPOSE
docker-compose -f lab2.yml up -d
cd /home/q/PY3
source bin/activate
echo "Creating MongoDb database and table and insert 10^N records"
time python lab2create.py
echo ""
echo "-------------------------------------------------------------"
echo ""
echo "Migrating table from MongoDb 1 to MongoDb 2"
time python lab2test.py
echo ""
echo "-------------------------------------------------------------"
echo ""
echo "Testing VERY BAD algoritm"
time python lab2algorithm.py
deactivate
cd ..
