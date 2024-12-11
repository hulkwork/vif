import pandas as pd
from .load_data import load_profile_data, load_fs1_data, load_ps2_data


def join_data(profile_path, fs1_path, ps2_path) -> pd.DataFrame:
    df_profile = load_profile_data(profile_path)
    df_profile["is_optimal"] = df_profile["valve_condition"].apply(
        lambda valve_condition: 1 if valve_condition == 100 else 0
    )

    df_fs1 = load_fs1_data(fs1_path)
    df_ps2 = load_ps2_data(ps2_path)

    merged_data = df_profile.join(df_fs1).join(df_ps2)
    return merged_data


def split_data(df: pd.DataFrame, n_split: int = 2000):
    return df[:n_split], df[n_split:]
