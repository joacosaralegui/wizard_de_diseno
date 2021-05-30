### This script is triggered from within docker contrainer
### to start multiple processes in the same container.
### This script is defined in the CMD option in Dockerfile
 
# Start actions server in background
python -m rasa_sdk --actions actions&
# Start rasa server with nlu model
rasa run --model /app/models --enable-api \
        --endpoints /app/endpoints.yml \
        --credentials /app/credentials.yml \
        -p $PORT \
        -d domain