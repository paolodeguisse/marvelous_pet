register-topic:
        docker compose exec kafka kafka-topics.sh --create --topic events --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2181

register-postgres:
        curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @register-postgres.json

list-kafka-topics:
        docker compose exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list

read-from-kafka-topic:
        docker compose exec kafka kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic events.public.events --from-beginning

delete-topic-kafka:
        docker compose exec kafka kafka-topics.sh --zookeeper zookeeper:2181 --delete --topic events.public.events
