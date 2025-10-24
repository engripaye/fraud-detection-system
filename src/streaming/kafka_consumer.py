import json
import joblib
from kafka import KafkaConsumer, KafkaProducer
import numpy as np
from redis_feature_store import RedisFeatureStore

MODEL_PATH = "src/model/rf_model.pkl"
SCALER_PATH = "src/model/scaler.pkl"


def load_model():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler


def main():
    model, scaler = load_model()
    consumer = KafkaConsumer(
        'transactions',
        bootstrap_servers=['kafka:9092'],
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        group_id='fraud_detector_group'
    )
    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
