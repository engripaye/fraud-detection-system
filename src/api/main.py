from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Fraud Detection System")
model = joblib.load("src/model/rf_model.pkl")


class Transaction(BaseModel):
    # include only v1...v28, scaled_amount, scaled_time
    v1: float
    v2: float
    v3: float
    v4: float
    v5: float
    v6: float
    v7: float
    v8: float
    v9: float
    v10: float
    v11: float
    v12: float
    v13: float
    v14: float
    v15: float
    v16: float
    v17: float
    v18: float
    v19: float
    v20: float
    v21: float
    v22: float
    v23: float
    v24: float
    v25: float
    v26: float
    v27: float
    v28: float
    scaled_amount: float
    scaled_time: float


@app.post("/predict")
def predict(tx: Transaction):
    arr = [getattr(tx, f"V{i}") for i in range(1, 29)]
    arr.append(tx.scaled_amount)
    arr.append(tx.scaled_time)
    X = np.array(arr).reshape(1, -1)
    score = model.predict_proba(X)[0, 1]
    return {"fraud_score": float(score)}

@app.get("/predict")    
