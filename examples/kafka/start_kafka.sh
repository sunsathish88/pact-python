#/bin/bash

docker-compose up -d

TOPIC_ID="mytopic"
echo "creating topic ${TOPIC_ID}"

docker-compose exec broker kafka-topics --create --topic ${TOPIC_ID} --bootstrap-server broker:9092 --replication-factor 1 --partitions 1