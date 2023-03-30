from kafka import KafkaConsumer
import psycopg2

settings = {
    "bootstrap_servers": "localhost:9092",
    "group_id": "group_id",
    "auto_offset_reset": "earliest"
}

def process_message(message):
    decoded_message = message.value.decode("utf-8")
    message_dict = eval(decoded_message)
    type_value = message_dict["type"]
    message_dict["type"] = type_value + " good job"

    conn = psycopg2.connect(
        host="ip",
        database="kafka_db",
        user="kafka_admin",
        password="pass"
    )

    cursor = conn.cursor()

    query = f"INSERT INTO result_table (button_id, type, dt, business_id) VALUES ({message_dict['button_id']}, '{message_dict['type']}', '{message_dict['dt']}>
    cursor.execute(query)

    conn.commit()
    cursor.close()
    conn.close()

topic = "events.public.events"

consumer = KafkaConsumer(topic, **settings)

for message in consumer:
    process_message(message)
