# create directory data if not exist
if [ ! -d data ]; then
    mkdir data
fi
sudo docker-compose up --build
