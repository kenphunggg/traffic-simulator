#!/bin/bash
user_count=$1

image_name="webapp"

# Create docker container
for ((i=1; i<=user_count; i++))
do
  port=$((28000 + i))
  docker run -d -p $port:8080 $image_name
done

# Generate the file to execute
python3 gen_code.py runtest $user_count

# Running the test
# locust -f runtest.py --headless -u 5 -r $user_count 5