import io
import pandas as pd
import requests
from datetime import datetime, timedelta
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def start_and_end_timestamp(days: int) -> tuple[int]:

    start_timestamp = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    end_timestamp = int(datetime.now().timestamp() * 1000)

    return start_timestamp, end_timestamp


def get_all_assets_ids() -> list[str]:
    response = requests.get(
        url="https://api.coincap.io/v2/assets/",
    ).json()

    assets_ids = [asset["id"] for asset in response["data"]]

    return assets_ids


def get_data_dict_from_asset_history(days: int) -> dict[str, list]:

    get_columns_flag = True
    assets_ids = get_all_assets_ids()
    start_timestamp, end_timestamp = start_and_end_timestamp(days)

    for asset in assets_ids:

        response = requests.get(
            url=f"https://api.coincap.io/v2/assets/{asset}/history",
            params={
                "interval": "m5",
                "start": start_timestamp,
                "end": end_timestamp,
            },
        ).json()

        if get_columns_flag:
            columns: list[str] = list(response["data"][0].keys()) + ["id"]
            data_dict = {k: [] for k in columns}
            get_columns_flag = False

        for asset_data_at_ts in response["data"]:
            for column in columns:
                if column != "id":
                    data_dict[column].append(asset_data_at_ts[column])
            data_dict["id"].append(asset)

    return data_dict



@data_loader
def load_data_from_api(*args, **kwargs):

    days = int(kwargs['days'])

    data_dict = get_data_dict_from_asset_history(days=days)

    return pd.DataFrame(data_dict), 'asset_history'


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'