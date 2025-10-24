import csv, json, time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def stream_from_csv(csv_path, topic="transactions", pause=0.1, limit=None):
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            tx = {k: v for k, v in row.items()}
            # ensure numeric types
            for k in list(tx.keys()):
                if k.startswith("V") or k in ("Amount", "Time"):
                    tx[k] = float(tx[k])
                tx["transaction_id"] = f"t_{count}"
                producer.send(topic, tx)
                count += 1
                if limit and count >= limit:
                    break
                time.sleep(pause)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/creditcard.csv")
    parser.add_argument("--limit", type=int, default=500)
    args = parser.parse_args()
    stream_from_csv(args.csv, limit=args.limit)


