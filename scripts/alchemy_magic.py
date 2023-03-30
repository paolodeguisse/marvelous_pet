from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class Result(Base):
    __tablename__ = 'result_table2'
    id = Column(Integer, primary_key=True)
    button_id = Column(Integer)
    type = Column(String)
    dt = Column(Date)
    business_id = Column(Integer)

def insert_into_result_table(message):
    message = json.loads(message.decode('utf-8'))
    button_id = message["button_id"]
    type = message["type"] + "bro_thats_working_good"
    dt = message["dt"]
    business_id = message["business_id"]
    engine = create_engine("postgresql://kafka_admin:some_pass@ip:5432/kafka_db")
    Session = sessionmaker(bind=engine)
    session = Session()
    new_record = Result(button_id=button_id, type=type, dt=dt, business_id=business_id)
    session.add(new_record)
    session.commit()
    session.close()

if __name__ == "__main__":


    engine = create_engine("postgresql://kafka_admin:some_pass@ip:5432/kafka_db")

    from kafka import KafkaConsumer

    settings = {
        "bootstrap_servers": "localhost:9092",
        "group_id": "group_id",
        "auto_offset_reset": "earliest"
    }

    topic = "events.public.events"

    consumer = KafkaConsumer(topic, **settings)

    Base.metadata.create_all(engine, checkfirst=True)

    for message in consumer:
        insert_into_result_table(message.value)
