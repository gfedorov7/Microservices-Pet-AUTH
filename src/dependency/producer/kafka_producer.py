import json

from fastapi import Depends
from kafka import KafkaProducer

from src.config import settings, KafkaSettings
from src.util.cache.cache import Cache
from src.util.cache.redis_cache import RedisCache
from src.util.producer.kafka_producer import MyKafkaProducer
from src.util.producer.producer import Producer


def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=settings.kafka_settings.kafka_advertised_listeners,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    )

def get_my_kafka_producer(
    kafka: KafkaProducer = Depends(get_kafka_producer),
) -> Producer:
    return MyKafkaProducer(kafka)