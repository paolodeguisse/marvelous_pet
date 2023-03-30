import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast
from transformers import BertTokenizer
from transformers import BertConfig, BertModel
import os
import pandas as pd

#tokenizer = BertTokenizerFast.from_pretrained('blanchefort/rubert-base-cased-sentiment-rusentiment')
#model = AutoModelForSequenceClassification.from_pretrained('blanchefort/rubert-base-cased-sentiment-rusentiment', return_dict=True)

models_path = u'/opt/kfk/cdc-kafka_postgres/ml/rubert-base-cased-sentiment-rusentiment'
tokenizer = BertTokenizerFast.from_pretrained(models_path)
model = AutoModelForSequenceClassification.from_pretrained(models_path, return_dict=True)


# initialize list of lists
data = [

        ['Здесь явно не пофлексишь',
         1],
        ['Кофе слегка горьковатый',
     3]

]




# Create the pandas DataFrame
df = pd.DataFrame(data, columns=['message_text', 'id'])

def predict(text):
    """0: NEUTRAL
    1: POSITIVE
    2: NEGATIVE"""
    inputs = tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**inputs)
    predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted = torch.argmax(predicted, dim=1).numpy()
    return predicted

df['sentiment'] = df['message_text'].apply(predict)
print(df)
