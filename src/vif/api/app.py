from typing import List, Union
import time
import os


import mlflow
import mlflow.sklearn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from vif.data_preparation.preprocess_data import join_data

app = FastAPI()

sample_data_paths = {
    "profile_path": os.environ["PROFILE_CSV"],
    "fs1_path": os.environ["FS1_CSV"],
    "ps2_path": os.environ["PS2_CSV"],
}
data = join_data(**sample_data_paths)
raw_data = data.drop(["valve_condition", "is_optimal"], axis="columns")
y_true = data["is_optimal"]

model = mlflow.sklearn.load_model(os.environ["MODEL_URI"])


class PredictionRequest(BaseModel):
    cycle_number: Union[int, List[int]]


class PredictionOutput(BaseModel):
    prediction: List[float]
    prediction_time: float


@app.post("/predict")
async def predict(request: PredictionRequest) -> PredictionOutput:
    try:
        start_time = time.time()
        cycle_number = request.cycle_number
        if isinstance(cycle_number, int):
            predict_data = raw_data.iloc[request.cycle_number].values.reshape(1, -1)
        if isinstance(cycle_number, list):
            predict_data = raw_data.iloc[request.cycle_number].values

        prediction = model.predict(predict_data)

        prediction_time = time.time() - start_time

        return {
            "prediction": prediction.tolist(),
            "prediction_time": prediction_time,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
