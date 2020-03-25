sudo docker stop postgres || true && sudo docker rm postgres || true
sudo docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=ganga -d postgres
sleep 10
echo "Running the python script now"
sudo /home/dumbmachine/anaconda3/bin/python postgres.py