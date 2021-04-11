from confluent_kafka import Producer
import sys
import random
import json

NAMES = ['Spot', 'Wolf', 'Winston', 'Tobey']
BREEDS = ['poodle', 'bulldog', 'Great Dane', 'Greyhound']

PRODUCER = Producer({'bootstrap.servers': 'localhost:9092'})

def acked(err, msg):
    if err is not None:
        print("Failed to deliver dog: {0}: {1}"
              .format(msg.value(), err.str()))
    else:
        print("Message produced: {0}".format(msg.value()))

class Dog():
    def __init__(self):
        i = random.randint(0, len(NAMES)-1)
        j = random.randint(0, len(BREEDS)-1)
        self.__type__ = 'dog'
        self.name = NAMES[i]
        self.breed = BREEDS[j]

    def __str__(self):
        return f'Name {self.name}, Breed {self.breed}'

def send_message(dog):
    print(dog)

    PRODUCER.produce('mytopic', json.dumps(dog.__dict__), callback=acked)
    PRODUCER.poll(0.5)

def main():
    number_of_dogs = int(sys.argv[1])

    try:
        for i in range(0, number_of_dogs):
            send_message(Dog())
        PRODUCER.flush(30)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
