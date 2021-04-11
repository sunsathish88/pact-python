"""pact test for a message consumer"""

import logging
import pytest
import json

from pact import MessageConsumer, Provider
from src.kafka_consumer import send_dog_event, send_dog_event_foo, CustomError

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PACT_BROKER_URL = "http://localhost"
PACT_BROKER_USERNAME = "pactbroker"
PACT_BROKER_PASSWORD = "pactbroker"
PACT_DIR = 'pacts'

CONSUMER_NAME = 'AnimalConsumer'
PROVIDER_NAME = 'DogProducer'

PACT_FILE = (f"{PACT_DIR}/{CONSUMER_NAME.lower().replace(' ', '_')}_message-"
             + f"{PROVIDER_NAME.lower().replace(' ', '_')}_message.json")

EXPECTED_DOG = {'type': 'dog', 'name': 'spot', 'breed': 'poodle'}

@pytest.fixture(scope='session')
def pact(request):
    version = request.config.getoption('--publish-pact')
    publish = True if version else False

    pact = MessageConsumer(CONSUMER_NAME, version=version).has_pact_with(
        Provider(PROVIDER_NAME),
        publish_to_broker=publish, broker_base_url=PACT_BROKER_URL,
        broker_username=PACT_BROKER_USERNAME, broker_password=PACT_BROKER_PASSWORD, pact_dir=PACT_DIR)

    yield pact


def test_assert_verify_message(pact):

    (pact
     .given('A dog created')
     .expects_to_receive('Spot the poodle')
     .with_content(str(json.dumps(EXPECTED_DOG)))
     .with_metadata({
         'Content-Type': 'application/json'
     })
     .verify(send_dog_event)
     )


def test_throw_exception_handler(pact):

    with pytest.raises(CustomError):
        (pact
            .given('A dog created')
            .expects_to_receive('Spot the poodle')
            .with_content(str(json.dumps({'type': 'cat', 'name': 'spot', 'breed': 'poodle'})))
            .with_metadata({
                'Content-Type': 'application/json'
            })
            .verify(send_dog_event))


def test_assert_dog_returned(pact):

    (pact
     .given('A dog created')
     .expects_to_receive('Spot the poodle')
     .with_content(str(json.dumps(EXPECTED_DOG)))
     .with_metadata({
         'Content-Type': 'application/json'
     })
     .verify(send_dog_event)
     )

    with pact:
        dog = pact.result
        assert dog.name == 'spot'
        assert dog.breed == 'poodle'


def test_assert_calling_dog(pact):

    (pact
     .given('A dog created')
     .expects_to_receive('Spot the poodle')
     .with_content(str(json.dumps(EXPECTED_DOG)))
     .with_metadata({
         'Content-Type': 'application/json'
     })
     )

    with pact:
        dog = send_dog_event_foo({}, str(json.dumps(EXPECTED_DOG)))
        assert dog.name == 'spot'
        assert dog.breed == 'poodle'
