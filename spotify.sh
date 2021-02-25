source /home/myer/Myaer/bin/activate
cd /home/myer/Myaer/Spotify
gunicorn spotify:spotify --bind localhost:8080 --worker-class aiohttp.GunicornWebWorker
