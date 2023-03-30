import logging
logging.basicConfig(level=logging.DEBUG)

settings = {
    "bootstrap_servers": "localhost:9092",
    "group_id": "group_id",
    "auto_offset_reset": "earliest"
}

topic = "events.public.events"

consumer = KafkaConsumer(topic, **settings)

for message in consumer:
    logging.debug(f"Received message: {message.value}")
    print(f"Received message: {message.value}")
