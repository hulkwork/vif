# VIF

# Predictive Maintenance - Valve Condition Model

This project implements a predictive maintenance system that predicts whether the valve condition is optimal based on sensor data. The system utilizes machine learning models (specifically a Random Forest) to analyze historical data and predict valve conditions.

## Table of Contents

- [VIF](#vif)
- [Predictive Maintenance - Valve Condition Model](#predictive-maintenance---valve-condition-model)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Folder tree](#folder-tree)
    - [.env file](#env-file)
    - [Install Dependencies](#install-dependencies)
  - [Running the Project](#running-the-project)
    - [Training the Model](#training-the-model)
    - [Running the API](#running-the-api)
    - [Running Unit Tests](#running-unit-tests)
  - [Docker (Under construction)](#docker-under-construction)
    - [Building the Images](#building-the-images)
      - [1. Build the Model Training Image:](#1-build-the-model-training-image)
      - [2. Build the API Image (TO-DO):](#2-build-the-api-image-to-do)
      - [3. Build the Unit Test Image:](#3-build-the-unit-test-image)
    - [Running the Containers](#running-the-containers)
      - [1. Run the Model Training Container:](#1-run-the-model-training-container)
      - [2. Run the API Container:](#2-run-the-api-container)
      - [3. Run the Unit Test Container:](#3-run-the-unit-test-container)

---

## Installation

### Prerequisites

- Python 3.10+
- Poetry (for dependency management)
- Docker (optional, for containerized environments)

### Folder tree 
```bash
├── data
│   ├── data_subset
│   └── data_subset.zip
├── Dockerfile
├── exploration
├── poetry.lock
├── pyproject.toml
├── README.md
├── sample.env
├── src
└── tests
```

### .env file
Put your config 
```bash
PROFILE_CSV=data/data_subset/data_subset/profile.txt
FS1_CSV=data/data_subset/data_subset/FS1.txt
PS2_CSV=data/data_subset/data_subset/PS2.txt
MODEL_URI=models:/random_forest_model/1
```

### Install Dependencies

Make sure you have [Poetry](https://python-poetry.org/docs/#installation) installed. You can install dependencies with:

```bash
poetry install
```

This will install all required dependencies, including those for development (tests, linters).

---

## Running the Project

The project is separated into three main components: model training, the API for serving predictions, and unit tests. Each component is handled separately using Docker, but can also be run locally.

### Training the Model

To train the model, use the following script. This will train the model and log the process using MLFlow.

```bash
export PYTHONPATH=$PWD:$PYTHONPATH
poetry run python src/vif/jobs/train_classifier.py
```
or 

```bash
export PYTHONPATH=$PWD:$PYTHONPATH
poetry run run-train
```

This will:
- Load and preprocess the data
- Train a RandomForest model
- Log the model in MLFlow
- Save the trained model locally

### Running the API

The FastAPI application serves the trained model and provides an endpoint to get predictions.

```bash
export PYTHONPATH=$PWD:$PYTHONPATH
poetry run uvicorn vif.api.app:app --host 0.0.0.0 --port 5000
```

This starts the FastAPI server, which can be accessed at `http://localhost:5000`.

To make a prediction, send a `POST` request to `/predict` with the `cycle_number` as JSON:

```json
{
  "cycle_number": 10
}
```
or 
```json
{
  "cycle_number": [10]
}
```

### Running Unit Tests

To run the unit tests, use Poetry with `pytest`:

```bash
export PYTHONPATH=$PWD:$PYTHONPATH
poetry run pytest
```

This will run all the tests located in the `tests` directory.

---

## Docker (Under construction)

The project uses multi-stage Docker builds to handle different tasks (training, API, testing). Below are the steps for building and running Docker images for each component.

### Building the Images

There are three build targets in the `Dockerfile`:

1. **Training**: For training the model.
2. **API**: For serving the API.
3. **Tests**: For running the unit tests.

To build the Docker image for each target, use the following commands:

#### 1. Build the Model Training Image:

```bash
docker build --target train -t predictive-maintenance-train .
```

This builds an image with all dependencies necessary for training the model.

#### 2. Build the API Image (TO-DO):

```bash
docker build --target api -t predictive-maintenance-api .
```

This builds an image for serving the FastAPI application with the trained model.

#### 3. Build the Unit Test Image:

```bash
docker build --target test -t predictive-maintenance-tests .
```

This builds an image that contains all necessary dependencies to run the tests.

### Running the Containers

Once the images are built, you can run the containers using the following commands:

#### 1. Run the Model Training Container:

```bash
docker run --rm -v $PWD/mlruns:/app/mlruns -v $PWD/data:/app/data predictive-maintenance-train
```

This runs the training process inside the container and logs the model.

#### 2. Run the API Container:

```bash
docker run -p 5000:5000 -v $PWD/mlruns:/app/mlruns -v $PWD/data:/app/data --rm predictive-maintenance-api
```

This runs the FastAPI application inside the container and exposes it on port 5000. You can now interact with the API.

#### 3. Run the Unit Test Container:

```bash
docker run --rm -v $PWD/data:/app/data predictive-maintenance-tests
```

This runs the unit tests inside the container and outputs the results to your terminal.

---

