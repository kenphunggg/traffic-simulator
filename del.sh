#!/bin/bash

# Get all running container IDs
container_ids=$(docker ps -q)

rm runtest.py

# Check if there are any running containers
if [ -z "$container_ids" ]; then
  echo "No running containers to delete."
  exit 0
fi

# Loop through each container ID and delete it
for container_id in $container_ids
do
  echo "Stopping container $container_id ..."
  sudo docker stop $container_id

  echo "Removing container $container_id ..."
  sudo docker rm $container_id
done


