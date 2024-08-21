import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def load_market_data_from_api(n_rows: int) -> dict[str, list]:

    url = f"https://api.coincap.io/v2/markets"
    columns_flag = True

    api_key = "6654350f-3734-4efe-905d-d113e40bc764"
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Authorization": f"Bearer {api_key}",
    }

    limit = 2000
    range_of_records = n_rows // limit

    for i in range(range_of_records):
        response = requests.get(
            url=url, params={"limit": limit, "offset": limit * i}, headers=headers
        ).json()

        if columns_flag:
            columns_flag = False

            columns = list(response["data"][0].keys()) + ["timestamp"]
            data_dict = {k: [] for k in columns}

        for crypto_data in response["data"]:

            for column, value in crypto_data.items():
                data_dict[column].append(value)

            data_dict["timestamp"].append(response["timestamp"])

    return data_dict


@data_loader
def load_data_from_api(*args, **kwargs):

    n_rows = int(kwargs['n_rows'])
    data_dict = load_market_data_from_api(n_rows=n_rows)

    return pd.DataFrame(data_dict), 'markets_data'


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
