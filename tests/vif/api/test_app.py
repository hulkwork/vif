# from fastapi.testclient import TestClient

# from src.vif.api.app import app

# client = TestClient(app)


# def test_predict_endpoint():
#     response = client.post("/predict", json={"cycle_number": [1]})
#     assert response.status_code == 200
#     json_response = response.json()
#     assert "prediction" in json_response
#     assert "prediction_time" in json_response
