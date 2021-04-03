# Introduction
A working example of Kafka and how you may use Pact to test your contracts

# Running the application
This example uses kafka and to see it working it uses the confluent docker images. Run
```sh
./start_kafka.sh
docker-compose ps  # checks that everything is running.
```
to bring it up and see all the images running. Navigate to http://localhost:9021 to see the Confluent Control Centre. You should be able to see 'mytopic' has been created.

Create two terminals. In one run
```sh
python kafka_consumer.py
```

You should see a message indicating Kafka has staretd. In the other run
```sh
python kafka_producer.py 10 # this param is the number of messages you want to create
```

You should see this window output a number of dogs and the other terminal receive them.

## Cleaning up
* Exit the running consumer window (Ctrl-C or keyboard interrupt)
* Run ./stop_kafka.sh in the terminal
* Check ```docker-compose ps``` to make sure Kafka has been stopped
* If you have finished you may want to run ./remove_kafka.sh to clean up some large images

# Running the tests
Run
```sh
pytest
```

