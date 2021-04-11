from confluent_kafka import Consumer, KafkaError
import json

settings = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'client.id': 'client-1',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
}
class Animal():
    def __init__(self, type, name, breed):
        self.type = type
        self.name = name
        self.breed = breed

    def __str__(self):
        return f'Animal {self.type}, Name {self.name}, Breed {self.breed}'

class CustomError(Exception):
    def __init__(self, *args):
        if args:
            self.topic = args[0]
        else:
            self.topic = None

    def __str__(self):
        if self.topic:
            return 'Custom Error:, {0}'.format(self.topic)


def message_decoder(obj):
    if 'type' in obj and obj['type'] == 'dog':
        return Animal('dog', obj['name'], obj['breed'])
    raise CustomError('type unknown')


def send_dog_event_foo(foo, payload):
    # ignoring foo here
    return send_dog_event(payload)


def send_dog_event(payload):
    dog = json.loads(payload, object_hook=message_decoder)
    print(dog)
    return dog

def start_consumer(kafka_consumer, topic):
    kafka_consumer.subscribe([topic])

    try:
        print("Starting Kafka...")
        while True:
            msg = kafka_consumer.poll(0.1)
            if msg is None:
                continue
            elif not msg.error():
                send_dog_event(msg.value())

            elif msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {0}/{1}'
                      .format(msg.topic(), msg.partition()))
            else:
                print('Error occured: {0}'.format(msg.error().str()))

    except KeyboardInterrupt:
        pass

    finally:
        kafka_consumer.close()


def main():
    c = Consumer(settings)
    start_consumer(c, 'mytopic')


if __name__ == "__main__":
    main()
