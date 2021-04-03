#/bin/bash

# clean up - kafka containers are quite large. If you need to prune these
docker system prune -a --volumes --filter "label=io.confluent.docker"