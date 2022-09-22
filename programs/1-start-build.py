# Pandas to manipulate the CSV files and data frames
import pandas as pd
import os

# clean out all csv files
if os.path.isfile('../csv/forex.csv'):
    os.remove("../csv/forex.csv")
    print("forex.csv removed")

    mydir = "../csv/working/"
    for f in os.listdir(mydir):
        os.remove(os.path.join(mydir, f))
    print("working files removed")

    mydir = "../csv/currency/"
    for f in os.listdir(mydir):
        os.remove(os.path.join(mydir, f))
    print("currency files removed")

# yfinance to download currency data from Yahoo
import yfinance as yf

# datetime to format dates
from datetime import date
from datetime import timedelta

# build currency comparison csv files from given currencies in the Ori.csv file
# Add Av5, Av10, Av30 columns for a 5, 10 & 30 day rolling average and to
# add the relative strength of the 2 currencies (inserted later)
# Log the list of currency comparisons to be used in the Forex.csv file

# Build Forex.csv to record currency comparisons used
column_names = ['ticker', 'currency']
df = pd.DataFrame(columns=column_names)
df.to_csv('../csv/forex.csv', index=False)

# Variables to select start and end dates to download data from Yahoo
numdays = 200
today = date.today()
start = today - timedelta(numdays)
td = str(today)
ts = str(start)

# use ori.csv for currencies to be used
df = pd.read_csv('../csv/ori.csv')
rn = len(df)

print('Building Forex list')

i = 0
while i < rn:

    # Get base currency
    mbase = df.loc[i, 'base']
    bcur = df.loc[i, 'currency']

    ii = i + 1
    while ii < rn:
        # skip 1 get quote currency
        mquote = df.loc[ii, 'base']
        qcur = df.loc[ii, 'currency']

        # download data from Yahoo
        data = yf.download(mbase + mquote + "=x", start=ts, end=td)
        df2 = pd.DataFrame(data)

        # insert extra columns to be use for rolling average
        df2.insert(6, "Av5", "0")
        df2.insert(7, "Av10", "0")
        df2.insert(8, "Av30", "0")

        df2['Av5'] = df2.iloc[:, 0].rolling(window=5).mean()
        df2['Av10'] = df2.iloc[:, 0].rolling(window=10).mean()
        df2['Av30'] = df2.iloc[:, 0].rolling(window=30).mean()

        rn2 = len(df2)
        tic = mbase + mquote + "=x"
        cur = bcur + '-' + qcur

        # if dataframe contains more than 5 records. ie not empty.
        # save as csv file use base as file name in working directory
        if rn2 > 5:
            df2.to_csv('../csv/working/' + tic + '.csv')
            df3 = pd.read_csv('../csv/forex.csv')

            # Add file name and description to forex master file
            row = [tic, cur]
            df3.loc[len(df3)] = row
            df3.to_csv('../csv/forex.csv', index=False)

        ii = ii + 1
    i = i + 1
