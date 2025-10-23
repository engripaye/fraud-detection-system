import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from features import load_data, preprocess, split


def train_and_save(data_path: str, model_path: str, scaler_path: str):
    df = load_data(data_path)
    X, y, scaler = preprocess(df)
    X_train, X_test, y_train, y_test = split(X, y)
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42, n_jobs=1)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]
    print(classification_report(y_test, preds, digits=4))
    print("ROC_AUC:", roc_auc_score(y_test, proba))
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print("Saved model and scaler.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/creditcard.csv")
    parser.add_argument("--model", default="src/model/rf_model.pkl")
    parser.add_argument("--scaler", default="src/model/scaler.pkl")
    args = parser.parse_args()
    train_and_save(args.data, args.model, args.scaler)
