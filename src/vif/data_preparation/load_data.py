import pandas as pd


def load_profile_data(path_profile: str) -> pd.DataFrame:
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


def load_fs1_data(path: str) -> pd.DataFrame:
    return pd.read_csv(
        path, delimiter="\t", names=[f"fs1_{i+1}x100Hz_bar" for i in range(600)]
    )


def load_ps2_data(path: str) -> pd.DataFrame:
    return pd.read_csv(
        path, delimiter="\t", names=[f"ps2_{i+1}x10Hz_l_per_min" for i in range(6000)]
    )
