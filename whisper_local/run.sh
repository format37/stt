# sudo docker run --gpus '"device=0"' -p 2700:2700 -t whisper
# Create folder ./cache if not exist
mkdir -p cache
sudo docker run --gpus '"device=0"' -p 2700:2700 -v $(pwd)/cache:/app/cache -t whisper