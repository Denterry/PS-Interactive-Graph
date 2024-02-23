# PS-Interactive-Graph
The graph illustrates cryptocurrency price information from May 2013 through October 2022. Using the Dashboard, you can select the cryptocurrency and the feature you want to illustrate.

## DataSet
This is a dataset of over 50 Cryptocurrencies' historical OHLC (Open High Low Close) data. The date range is from May 2013 to October 2022 on a daily basis.

The data was borrowed from Kaggle datasets: https://www.kaggle.com/datasets/maharshipandya/-cryptocurrency-historical-prices-dataset?resource=download

**Column Description**
- open: Opening price on that particular date (UTC time)
- high: Highest price hit on that particular date (UTC time)
- low: Lowest price hit on that particular date (UTC time)
- close: Closing price on that particular date (UTC time)
- volume: Quantity of asset bought or sold, displayed in base currency
- marketCap: The total value of all the coins that have been mined. It's calculated by multiplying the number of
- coins in circulation by the current market price of a single coin
- timestamp: UTC timestamp of the day considered
- crypto_name: Name of the cryptocurrency
- date: timestamp converted to date

## Launching
```
$ python3 praph.py
```
Dashboard you can find on the ``` http://127.0.0.1:8050/ ```