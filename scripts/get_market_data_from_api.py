import requests


def load_data_from_api(n_rows: int) -> dict[str, list]:

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


def main() -> None:
    import pandas as pd

    data_dict = load_data_from_api(n_rows=50000)
    df = pd.DataFrame(data_dict)
    df.to_csv('markets.csv')
    print(df.shape)
    print(df.tail())


if __name__ == "__main__":
    main()
