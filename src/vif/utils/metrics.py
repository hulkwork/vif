from typing import Dict
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score


def evaluate_classification(y_true, y_pred) -> Dict[str, float]:
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
    }
    return metrics
