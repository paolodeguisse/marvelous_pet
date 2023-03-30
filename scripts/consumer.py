import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast
from transformers import BertTokenizer
from transformers import BertConfig, BertModel
import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import logging
import numpy as np

Base = declarative_base()

class Result(Base):
    __tablename__ = 'sentiment_v2'
    id = Column(Integer, primary_key=True)
    button_id = Column(Integer)
    type = Column(String)
    sentiment_predict = Column(String)
    dt = Column(Date)
    business_id = Column(Integer)

def predict(text):
    """0: NEUTRAL
    1: POSITIVE
    2: NEGATIVE"""
    inputs = tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**inputs)
    predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted = torch.argmax(predicted, dim=1).numpy()
    return predicted

def insert_into_result_table(message):
    message = json.loads(message.decode('utf-8'))
    button_id = message["button_id"]
    type = message["type"]
    dt = message["dt"]
    business_id = message["business_id"]

    # добавляем вызов функции predict на поле type
    predicted_message = predict(type)

    Session = sessionmaker(bind=engine)
    session = Session()
    new_record = Result(button_id=button_id, type=type, sentiment_predict=np.array2string(predicted_message), dt=dt, business_id=business_id)
    session.add(new_record)
    session.commit()
    session.close()

    logging.info('[x] message is ready!')

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    models_path = u'/opt/marvelous_pet/rubert-base-cased-sentiment-rusentiment'
    tokenizer = BertTokenizerFast.from_pretrained(models_path)
    model = AutoModelForSequenceClassification.from_pretrained(models_path, return_dict=True)

    engine = create_engine("postgresql://kafka_admin:hey_boy_dont_look_at_my_password_!@ip:5432/kafka_db")

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

