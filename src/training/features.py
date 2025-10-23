import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(path: str):
    df = pd.read_csv(path)
    return df


def preprocess(df: pd.DataFrame):
    # Kaggle dataset: Column v1...v28, Time, amount, class
    df = df.copy()
    # scale Amount and Time
    scaler = StandardScaler()
    df[['scaled_amount', 'scaled_time']] = scaler.fit_transform(df[['Amount', 'Time']])
    X = df.drop(Columns=['Time', 'Amount', 'Class'])
    y = df['class']
    return X, y, scaler


def split(X, y, text_size=0.2, random_state=42):
    return train_test_split(X, y, text_size=text_size, stratify=y, random_state=random_state)
