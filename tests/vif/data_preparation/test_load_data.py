import dotenv
import os
import pytest
import pandas as pd


dotenv.load_dotenv()

from src.vif.data_preparation.load_data import (
    load_profile_data,
    load_fs1_data,
    load_ps2_data,
)


@pytest.fixture
def sample_profile_data():
    return os.environ["PROFILE_CSV"]


@pytest.fixture
def sample_fs1_data():
    return os.environ["FS1_CSV"]


@pytest.fixture
def sample_ps2_data():
    return os.environ["PS2_CSV"]


def test_load_profile_data(sample_profile_data):
    df = load_profile_data(sample_profile_data)
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == [
        "cooler_condition",
        "valve_condition",
        "internal_pump_leakage",
        "hydraulic_accumulator_bar",
        "stable_flag",
    ]


def test_load_fs1_data(sample_fs1_data):
    df = load_fs1_data(sample_fs1_data)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[1] == 600


def test_load_ps2_data(sample_ps2_data):
    df = load_ps2_data(sample_ps2_data)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[1] == 6000
