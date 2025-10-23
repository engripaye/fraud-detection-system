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

