from datetime import datetime, timedelta
import requests
import pandas as pd


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


def get_all_exchange_ids() -> list[str]:
    response = requests.get(
        url='https://api.coincap.io/v2/exchanges/',
    ).json()

    exchange_ids = list(set([ex_info['exchangeId'] for ex_info in response['data']]))

    return exchange_ids


def get_data_dict_from_candles(days: int) -> dict[str, list]:

    get_columns_flag = True
    assets_ids = get_all_assets_ids()
    exchange_ids = get_all_exchange_ids()
    quoteId = 'bitcoin'
    start_timestamp, end_timestamp = start_and_end_timestamp(days)

    for exchange in exchange_ids:
        for asset in assets_ids:

            response = requests.get(
                url=f"https://api.coincap.io/v2/candles",
                params={
                    "interval": "m5",
                    "start": start_timestamp,
                    "end": end_timestamp,
                    'exchange': exchange,
                    'quoteId': quoteId,
                    'baseId': asset,
                },
            ).json()

            if len(response['data']) == 0:
                continue


            if get_columns_flag:
                print(response)
                columns: list[str] = list(response["data"][0].keys()) + ["baseId", 'quoteId', 'exchange']
                print(columns)
                data_dict = {k: [] for k in columns}
                get_columns_flag = False

            for asset_data_at_ts in response["data"]:
                for column in columns:
                    if column not in ("baseId", 'quoteId', 'exchange'):
                        data_dict[column].append(asset_data_at_ts[column])
                data_dict["baseId"].append(asset)
                data_dict["quoteId"].append(quoteId)
                data_dict["exchange"].append(exchange)

    return data_dict


def main() -> None:
    data_dict = get_data_dict_from_candles(2)
    df = pd.DataFrame(data_dict)
    print(df.head())


if __name__ == '__main__':
    main()
