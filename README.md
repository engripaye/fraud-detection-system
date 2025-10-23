---
# 🚨 Fraud Detection System — Real-Time ML & Streaming with Python, Kafka & Redis

Detect fraudulent credit card transactions in **real time** using **Machine Learning, Kafka streaming, Redis caching**, and **FastAPI model serving**.
This project demonstrates the full end-to-end lifecycle of a production-ready fraud detection pipeline — from data preprocessing and model training to real-time inference and API deployment.

---

## 🧠 Overview

| Area                      | Technology                            |
| ------------------------- | ------------------------------------- |
| **Language**              | Python 3.10+                          |
| **Machine Learning**      | scikit-learn (RandomForestClassifier) |
| **Streaming**             | Apache Kafka                          |
| **Feature Store / Cache** | Redis                                 |
| **API Service**           | FastAPI                               |
| **Containerization**      | Docker + Docker Compose               |

---

## 🌟 Why This Project Stands Out

✅ Demonstrates **end-to-end ML engineering** — data preprocessing, training, and real-time model serving.
✅ Integrates **Kafka** for real-time streaming and **Redis** for low-latency feature retrieval.
✅ Deployable with **Docker Compose** for easy local or cloud testing.
✅ Includes a **REST API** for live prediction requests.
✅ Great showcase for **data engineering, MLOps, and software design** skills.

---

## 🏗️ Architecture

```
+------------------+
|   Kaggle Data    |
|  (creditcard.csv)|
+--------+---------+
         |
         v
+------------------+     +---------------------+
|   Training Job   |-->  |   Trained Model     |
| (scikit-learn RF)|     |  rf_model.pkl       |
+--------+---------+     +----------+----------+
         |                           |
         v                           v
+------------------+         +------------------+
| Kafka Producer   |  --->   | Kafka Consumer   |
| (streams txns)   |         | (fraud detector) |
+------------------+         +------------------+
                                   |
                                   v
                           +----------------+
                           | Redis Cache    |
                           +----------------+
                                   |
                                   v
                            +---------------+
                            | FastAPI API   |
                            | /predict      |
                            +---------------+
```

---

## 🧩 Features

* **Offline Training**: RandomForest model trained on Kaggle’s credit card dataset.
* **Real-Time Streaming**: Kafka producer sends transactions → consumer performs fraud scoring.
* **Feature Store**: Redis used to cache and retrieve user-level features.
* **REST API**: FastAPI endpoint `/predict` for real-time predictions.
* **Containerized Deployment**: One-command setup via Docker Compose.

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/fraud-detection-system.git
cd fraud-detection-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Download Dataset

Get the dataset from [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/mlg-ulb/creditcardfraud)
Save it to:

```
data/creditcard.csv
```

---

## 🧠 Model Training

Train and export the RandomForest model:

```bash
python src/training/train.py --data data/creditcard.csv
```

✅ Output example:

```
precision    recall  f1-score   support
0       0.99      1.00      0.99    56863
1       0.95      0.83      0.89       99
ROC AUC: 0.985
Saved model and scaler.
```

Model artifacts will be stored in:

```
src/model/rf_model.pkl
src/model/scaler.pkl
```

---

## 🚀 Run the System (Full Pipeline)

### 1️⃣ Start Services

```bash
docker-compose -f docker/docker-compose.yml up --build
```

This starts **Kafka**, **Zookeeper**, **Redis**, and your **FastAPI app**.

### 2️⃣ Start Kafka Consumer

```bash
python src/streaming/kafka_consumer.py
```

### 3️⃣ Stream Transactions

```bash
python src/streaming/kafka_producer.py --csv data/creditcard.csv --limit 20
```

✅ You’ll see:

```
Processed: {'transaction_id': 't_0', 'user_id': 'unknown', 'fraud_score': 0.0021}
Processed: {'transaction_id': 't_1', 'user_id': 'unknown', 'fraud_score': 0.9875}
...
```

---

## 🌐 REST API Testing

### Run FastAPI locally

```bash
uvicorn src.api.main:app --reload
```

Then visit:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

Use the `/predict` endpoint with this sample payload:

```json
{
  "V1": -1.3598, "V2": -0.0728, "V3": 2.5363, "V4": 1.3782, "V5": -0.3383,
  "V6": 0.4624, "V7": 0.2396, "V8": 0.0987, "V9": 0.3638, "V10": 0.0903,
  "V11": -0.5516, "V12": -0.6178, "V13": -0.9913, "V14": -0.3112, "V15": 1.4682,
  "V16": -0.4704, "V17": 0.2079, "V18": 0.0258, "V19": 0.4037, "V20": 0.2514,
  "V21": -0.0183, "V22": 0.2778, "V23": -0.1105, "V24": 0.0669, "V25": 0.1285,
  "V26": 0.0110, "V27": 0.2785, "V28": 0.0638,
  "scaled_amount": 0.015, "scaled_time": 0.02
}
```

✅ Response:

```json
{ "fraud_score": 0.0034 }
```

---

## 🧪 Testing & Validation

| Test              | Command                                  | Description            |
| ----------------- | ---------------------------------------- | ---------------------- |
| **Train model**   | `python src/training/train.py`           | Train & save model     |
| **API test**      | `uvicorn src.api.main:app`               | Test REST `/predict`   |
| **Kafka test**    | `python src/streaming/kafka_producer.py` | Stream transactions    |
| **Consumer test** | `python src/streaming/kafka_consumer.py` | Process fraud scores   |
| **Unit tests**    | `pytest`                                 | Validate model + logic |

---

## 📊 Example Output

| Transaction ID | Fraud Score |
| -------------- | ----------- |
| t_001          | 0.0031      |
| t_002          | 0.9824      |
| t_003          | 0.0065      |

---

## 🧱 Folder Structure

```
fraud-detection/
├─ data/
│  └─ creditcard.csv
├─ src/
│  ├─ api/              # FastAPI inference service
│  ├─ model/            # Saved model/scaler
│  ├─ training/         # Data prep + model training
│  ├─ streaming/        # Kafka producer/consumer + Redis
│  └─ utils/            # Extra metrics/utils
├─ docker/
│  ├─ Dockerfile.app
│  └─ docker-compose.yml
├─ notebooks/           # Optional EDA or feature exploration
├─ requirements.txt
└─ README.md
```

---

## 🧩 Technologies Used

* **Python** — core programming language
* **scikit-learn** — ML training and evaluation
* **Kafka** — event streaming
* **Redis** — feature store/cache
* **FastAPI** — REST API for real-time prediction
* **Docker** — containerized environment

---

## 🔮 Future Improvements

* Replace RandomForest with **PyTorch TabNet / XGBoost** for better performance
* Add **drift detection** and **auto-retraining pipeline**
* Integrate **Prometheus & Grafana** for monitoring
* Deploy to **Kubernetes** for scalability
* Add **frontend dashboard** for live fraud visualization

---

## 🧑‍💻 Author

**Olabowale Ipaye**
🎯 Fullstack Backend Developer | Devops Engineer
📍 Nigeria
🔗 [LinkedIn Profile](https://www.linkedin.com/in/engripayebabatunde)
💻 [GitHub](https://github.com/engripaye)

---
