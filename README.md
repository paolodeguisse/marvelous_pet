Step 1, run the docker compose
```
docker compose up -d
```

Step 2, Start the Debezium connector
 ```
apt update -y && \
apt install python3-pip -y
pip install kafka-python
pip install torch
pip install transformers
pip install pandas
pip install pyspark
apt install rustc
pip install -U setuptools
apt install git-lfs
git lfs install
git clone https://huggingface.co/blanchefort/rubert-base-cased-sentiment-rusentiment
pip3 install psycopg2-binary
pip3 install sqlalchemy
```

after this 100% you need to do this:
 ```
register-postgres:
        curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @register-postgres.json
 ```

if logs of Kafka show DNS problems:
 ```
nano /etc/hosts
127.0.0.1 kafka
 ```
