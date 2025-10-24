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

    rfs = RedisFeatureStore()
    for msg in consumer:
        tx = msg.value
        # tx is expected to contain v1...v28, scaled_amount, scaled_time, maybe user_id
        user_id = tx.get("user_id", "unknown")
        user_feats = rfs.get_user_features(user_id)
        # merge features (simple example)
        feat_vec = []
        for col in sorted([c for c in tx.keys() if c.startswith("v")]) :
            feat_vec.append(tx[col])
        # append scaled_amount/time if present
        feat_vec.append(tx.get("scaled_amount", 0.0))
        feat_vec.append(tx.get("scaled_time", 0.0))
        X = np.array(feat_vec).reshape(1, -1)
        score = model.predict_proba(X)[0,1]
        out = {"transaction_id": tx.get("transaction_id"), "user_id": user_id, "fraud_score": float(score)}
        producer.send("fraud_scores", out)
        print("Processed:", out)


if __name__ == "__main__":
    main()