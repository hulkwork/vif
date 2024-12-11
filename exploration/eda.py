import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
from typing import Tuple
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    accuracy_score,
)


def load_profile_data(
    path_profile: str = "data/data_subset/data_subset/profile.txt",
) -> pd.DataFrame:
    return pd.read_csv(
        path_profile,
        delimiter="\t",
        names=[
            "cooler_condition",
            "valve_condition",
            "internal_pump_leakage",
            "hydraulic_accumulator_bar",
            "stable_flag",
        ],
    )


def load_fs1_data(path: str = "data/data_subset/data_subset/FS1.txt") -> pd.DataFrame:
    return pd.read_csv(
        path, delimiter="\t", names=[f"fs1_{i+1}x100Hz_bar" for i in range(600)]
    )


def load_ps2_data(
    path: str = "data/data_subset/data_subset/PS2.txt",
) -> pd.DataFrame:
    return pd.read_csv(
        path, delimiter="\t", names=[f"ps2_{i+1}x10Hz_l_per_min" for i in range(6000)]
    )


def join_data() -> pd.DataFrame:
    df_profile = load_profile_data()
    df_profile["is_optimal"] = df_profile["valve_condition"].apply(
        lambda valve_condition: 1 if valve_condition == 100 else 0
    )

    df_fs1 = load_fs1_data()

    df_ps2 = load_ps2_data()
    merged_data = df_profile.join(df_fs1)
    merged_data = merged_data.join(df_ps2)
    return merged_data


def split_data(
    df: pd.DataFrame, n_split: int = 2000
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return df[:n_split], df[n_split:]


if __name__ == "__main__":
    merged_data = join_data()
    train, test = split_data(merged_data, n_split=2000)

    X_train = train.drop(["valve_condition", "is_optimal"], axis="columns")
    y_train = train["is_optimal"]
    X_test = test.drop(["valve_condition", "is_optimal"], axis="columns")
    y_test = test["is_optimal"]

    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)

    with mlflow.start_run():
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        accuracy = accuracy_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)

        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
        print(f"F1-Score: {f1}")
        print(f"Accuracy: {accuracy}")
        print(f"Confusion Matrix:\n{conf_matrix}")

        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("random_state", 42)

        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("accuracy", accuracy)

        signature = infer_signature(X_test, y_pred)

        mlflow.sklearn.log_model(model, "random_forest_classifier", signature=signature)
