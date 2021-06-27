import pandas as pd
import datetime as dt

trade_hour = 19  # hourly data - pick hour of buy sell e.g. 19 = 19:00
from_date = dt.datetime(2021,1,1)  # from which date to run the data

df = pd.read_csv('data.csv', parse_dates=['Date'])
df = df[df.Date > from_date]
df = df[df.Date.dt.hour == trade_hour]
df.reset_index(drop=True, inplace=True)

rows = df.shape[0]

prices = []
pair = [0,0]

for i in range(rows):
    if df.at[i,'Date'].weekday() == 4:
        pair[0] = float(df.at[i,'Close'])

    if df.at[i,'Date'].weekday() == 0:
        if pair[0] == 0:
            continue
        pair[1] = float(df.at[i,'Close'])
        prices.append(pair.copy())



cash = 100

for item in prices:
    print(f"Start Cash {cash:.4f} Buy:{item[0]} Sell:{item[1]}")
    cash = cash * (item[1]/item[0])
    print(f"End Cash {cash:.4f}")

print(f"{cash:.4f}")
