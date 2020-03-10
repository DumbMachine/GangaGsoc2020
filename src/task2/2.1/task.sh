echo "removing MongoDB docker container if it exists already"
sudo docker ps -q --filter "name=mongo" | grep -q . && sudo docker stop mongo && docker rm -fv mongo
echo "Starting the MongoDB docker container"
sudo docker run --name mongo -p 27017:27017 -d mongo;
python task2_1.py
sudo docker stop mongo; sudo docker rm mongo;
echo "Shut and Removed MongoDB docker container"