import io
import pandas as pd
import requests
from time import sleep
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    
    # url = args.url
    # n_rows = int(args.n_rows)
    # dirc = args.dir

    url = 'https://' + 'api.coincap.io/v2/assets'
    n_rows = 1000
    columns_flag = True

    while True:
        # response = requests.get(f"https://{url}" if 'https://' not in url else url).json()
        response = requests.get(url).json()
        # pprint(response["data"][0])
        # print(response["timestamp"])
        
        if columns_flag:
            columns_flag = False

            columns = list(response["data"][0].keys()) + ["timestamp"]
            data_dict = {k: [] for k in columns}

        for crypto_data in response["data"]:
            
            for column, value in crypto_data.items():
                data_dict[column].append(value)
                
            data_dict["timestamp"].append(response["timestamp"])

        sleep(0.5)

        if len(data_dict["timestamp"]) >= n_rows:
            df = pd.DataFrame(data_dict)
            break
    
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'