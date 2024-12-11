import pytest
import pandas as pd
import os
import dotenv

dotenv.load_dotenv()

from src.vif.data_preparation.preprocess_data import join_data, split_data


@pytest.fixture
def sample_data_paths():
    return {
        "profile_path": os.environ["PROFILE_CSV"],
        "fs1_path": os.environ["FS1_CSV"],
        "ps2_path": os.environ["PS2_CSV"],
    }


def test_join_data(sample_data_paths):
    data = join_data(**sample_data_paths)
    assert isinstance(data, pd.DataFrame)
    assert "is_optimal" in data.columns
    assert data.shape[1] > 6000


def test_split_data():
    df = pd.DataFrame({"col1": range(10), "col2": range(10)})
    train, test = split_data(df, n_split=7)
    assert len(train) == 7
    assert len(test) == 3
