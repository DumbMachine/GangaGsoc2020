sudo docker stop mongo; sudo docker rm mongo;
sudo docker stop postgres; sudo docker rm postgres;

sudo docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=ganga -d postgres
sudo docker run --name mongo -p 27017:27017 -d mongo;

ganga full_print_method.py
ganga full_print_method_postgres.py
