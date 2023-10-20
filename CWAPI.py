import requests
import os
from time import sleep
from time import time
import pandas as pd
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '15',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '815f0f17-dfe9-493b-b39d-60799b08fc5c',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

    # json normalizing

df = pd.json_normalize(data['data'])

df['timestamp'] = pd.to_datetime('now')  # takes an actual time of running


def api_runner():
    global df
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '15',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '815f0f17-dfe9-493b-b39d-60799b08fc5c',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    df2 = pd.json_normalize(data['data'])

    df2['timestamp'] = pd.to_datetime('now')  # takes an actual time of running
    df = df._append(df2)  # adding to the original dataframe

    if not os.path.isfile(r"C:\Users\USER\Desktop\python DA\CryptoWebAPI\CWAPI.csv"):
        df.to_csv(
            r"C:\Users\USER\Desktop\python DA\CryptoWebAPI\CWAPI.csv", header='column_names')
    else:
        df.to_csv(r"C:\Users\USER\Desktop\python DA\CryptoWebAPI\CWAPI.csv",
                  mode='a', header=False)


# tracking time and calling api_runner function how I want

for i in range(333):  # 333 -because I got 333 runs per day due to API systems
    api_runner()  # calling API
    print('API is running. Get you crypto data freely!')
    sleep(3600)  # sleep for 1h


df99 = pd.read_csv(r"C:\Users\USER\Desktop\python DA\CryptoWebAPI\CWAPI.csv")

pd.set_option('display.float_format', lambda x: '%.5f' % x)

df99 = df99.groupby('name', sort=False)[
    ['quote.USD.percent_change_1h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d']].mean()

df99 = df99.stack()

df99 = df99.to_frame(name='values')

df99 = df99.reset_index()

df99 = df99.rename(columns={'level_1': 'percent_change'})


sns.catplot(x='percent_change', y='values', hue='name', data=df99, kind='bar')


df99['percent_change'] = df99['percent_change'].replace(
    ['quote.USD.percent_change_1h'], ['1h'])
df99['percent_change'] = df99['percent_change'].replace(
    ['quote.USD.percent_change_24h'], ['24h'])
df99['percent_change'] = df99['percent_change'].replace(
    ['quote.USD.percent_change_7d'], ['7d'])
sns.catplot(x='percent_change', y='values',
            hue='name', data=df99, kind='point')


df10 = df[['name', 'quote.USD.percent_change_24h', 'timestamp']]
# df10 = df10.query("name == 'Bitcoin'")

# df10['timestamp'] = pd.to_datetime(df10['timestamp'], utc=True)

# sns.set_theme(style='darkgrid')
# sns.lineplot(x='timestamp', y='quote.USD.percent_change_24h', data=df10)
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
# plt.gcf().autofmt_xdate()

print(df10)
print(df99)
plt.show()
