import requests
from pprint import pprint
import time
import pandas as pd
import argparse
from argparse import Namespace


def main(args: Namespace) -> None:

    columns_flag = True
    
    url = args.url
    n_rows = int(args.n_rows)
    dirc = args.dir

    while True:
        response = requests.get(f"https://{url}" if 'https://' not in url else url).json()
        pprint(response["data"][0])
        print(response["timestamp"])
        
        if columns_flag:
            columns_flag = False

            columns = list(response["data"][0].keys()) + ["timestamp"]
            data_dict = {k: [] for k in columns}

        for crypto_data in response["data"]:
            
            for column, value in crypto_data.items():
                data_dict[column].append(value)
                
            data_dict["timestamp"].append(response["timestamp"])

        time.sleep(0.5)

        if len(data_dict["timestamp"]) >= n_rows:

            df = pd.DataFrame(data_dict)
            print(df.head())
            name = url.split("/")[-1]
            df.to_csv(f"{dirc}/{name}.csv", index=False)
            break


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Argument Parser")
    
    parser.add_argument("--url", required=True)
    parser.add_argument("--n_rows", required=True)
    parser.add_argument("--dir", required=True)

    args = parser.parse_args()
    main(args)
