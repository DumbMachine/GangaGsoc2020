echo "Starting the MongoDB docker container"
sudo docker run --name mongo -p 27017:27017 -d mongo;
python task2_1.py
sudo docker stop mongo; sudo docker rm mongo;
echo "Shut and Removed MongoDB docker container"