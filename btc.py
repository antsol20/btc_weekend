import pandas as pd
import datetime as dt
import requests

with open("apikey.txt", "r") as keyfile:
    apikey = keyfile.readline()

start_str = input("Enter start date in YYYYMMDD :")
end_str = input("Enter end date in YYYYMMDD :")

datefmt_in = '%Y%m%d'
datefmt = '%Y-%m-%dT%H:%M:%SZ'
url = 'https://api.nomics.com/v1/exchange-rates/history'
start_dt = dt.datetime.strptime(start_str, datefmt_in)
end_dt = dt.datetime.strptime(end_str, datefmt_in)

params = {'key': apikey, 'currency': 'BTC', 'start': start_dt.strftime(datefmt), 'end': end_dt.strftime(datefmt)}
response = requests.get(url=url, params=params)
json = response.json()

df = pd.DataFrame.from_dict(json)

rows = df.shape[0]
prices = []
pair = [0, 0]

for i in range(rows):
    stamp_dt = dt.datetime.strptime(df.at[i, 'timestamp'], datefmt)
    if stamp_dt.weekday() == 4:
        pair[0] = float(df.at[i, 'rate'])

    if stamp_dt.weekday() == 0:
        if pair[0] == 0:
            continue
        pair[1] = float(df.at[i, 'rate'])
        prices.append(pair.copy())


cash = 100

for item in prices:
    print(f"Start Cash {cash:.4f} Buy:{item[0]} Sell:{item[1]}")
    cash = cash * (item[1]/item[0])
    print(f"End Cash {cash:.4f}")

print(f"Total Return : cd {cash:.4f}")
