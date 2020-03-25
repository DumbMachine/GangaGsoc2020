sudo docker stop mongo || true && sudo docker rm mongo || true
sudo docker run --name mongo -p 27017:27017 -d mongo;
echo "Running the python script now"
sudo /home/dumbmachine/anaconda3/bin/python mongo.py