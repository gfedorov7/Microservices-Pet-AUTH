from typing import Any, Dict
import json

from kafka import KafkaProducer

from src.util.producer.producer import Producer


class MyKafkaProducer(Producer):
    def __init__(self, producer: KafkaProducer):
        self.producer = producer

    def send(self, title: str, payload: Dict[str, Any]):
        self.producer.send(title, payload)
        self.producer.flush()