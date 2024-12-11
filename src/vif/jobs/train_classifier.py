import os
from dotenv import load_dotenv

import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature


from src.vif.data_preparation.preprocess_data import join_data, split_data
from src.vif.modeling.train_model import train_model
from src.vif.utils.metrics import evaluate_classification

load_dotenv()


def main():
    sample_data_paths = {
        "profile_path": os.environ["PROFILE_CSV"],
        "fs1_path": os.environ["FS1_CSV"],
        "ps2_path": os.environ["PS2_CSV"],
    }
    data = join_data(**sample_data_paths)
    print(data.shape)
    train, test = split_data(data, n_split=2000)

    X_train = train.drop(["valve_condition", "is_optimal"], axis="columns")
    y_train = train["is_optimal"]
    X_test = test.drop(["valve_condition", "is_optimal"], axis="columns")
    y_test = test["is_optimal"]
    params = {"n_estimators": 100}
    print(X_train.shape)
    model = train_model(
        X_train=X_train, y_train=y_train, n_estimators=params["n_estimators"]
    )
    with mlflow.start_run():
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        metrics = evaluate_classification(y_test, y_pred=y_pred)
        for key in metrics:
            print(f"{key} : {metrics[key]}")
            mlflow.log_metric(key, metrics[key])

        signature = infer_signature(X_test, y_pred)

        mlflow.sklearn.log_model(
            model,
            artifact_path="model",
            registered_model_name="random_forest_model",
            signature=signature,
        )


if __name__ == "__main__":
    main()
