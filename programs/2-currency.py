import pandas as pd
from datetime import date
from datetime import timedelta

numdays = 210
today = date.today()
start = today - timedelta(numdays)
td = str(today)
ts = str(start)

# build currency files to record currency relative strength
# Calculate Currency strength based on percentage rise or fall of average closing price
# from the ori file build a csv file for each currency being used

df = pd.read_csv('../csv/ori.csv')
rn = len(df)
i = 0

while i < rn:
    x = df.loc[i, 'base']
    column_names = ["Date", "No", "RiseFall"]
    df2 = pd.DataFrame(columns=column_names)

    # add dates to currency file
    datecount = numdays
    today = date.today()
    start = today - timedelta(datecount)
    td = str(today)
    ts = str(start)

    while start <= today:
        df2 = df2.append({'Date': ts, 'No': 0, 'RiseFall': 0}, ignore_index=True)
        datecount = datecount - 1
        start = today - timedelta(datecount)
        ts = str(start)

    # delete Saturdays and Sundays
    df2['Date'] = pd.to_datetime(df2['Date'], format='%Y-%m-%d', errors='ignore')
    df2['day_of_week'] = df2['Date'].dt.strftime('%A')
    df2.drop(df2[df2['day_of_week'] == 'Saturday'].index, inplace=True)
    df2.drop(df2[df2['day_of_week'] == 'Sunday'].index, inplace=True)
    print(x + ' Built')

    df2.to_csv('../csv/currency/' + x + '.csv', index=False)

    i = i + 1

# using the forex file get the closing price of each currency pair
df = pd.read_csv('../csv/forex.csv')
rn = len(df)
i = 0

print('Calculating currency relative strength')
while i < rn:
    mtic = df.loc[i, 'ticker']
    print(mtic)

    # the first 3 characters are the base currency and 4th to 6th characters are the quote currency
    mbase = str(mtic)[0:3]
    mquote = str(mtic)[3:6]
    dd = str(i)
    dd2 = str(rn)
    print(dd + ' of ' + dd2)

    # using the 2 different currency files and the comparison file.
    df2 = pd.read_csv('../csv/working/' + mtic + '.csv')
    df3 = pd.read_csv('../csv/currency/' + mbase + '.csv')
    df4 = pd.read_csv('../csv/currency/' + mquote + '.csv')

    # calculate average closing price of the comparison file
    mmax = df2['Close'].max()
    mmin = df2['Close'].min()
    mav = (mmax + mmin) / 2

    i2 = 0
    rn2 = len(df2)
    while i2 < rn2:
        mdate = df2.loc[i2, 'Date']
        mclose = df2.loc[i2, 'Close']

        # If the closing price and the average price are equal declare values 0 to avoid a NaN
        mdif = mclose - mav
        if mdif == 0:
            mpbase = 0
            mpquote = 0
        else:
            # Calculate base % move from average
            mv3 = mav / mdif
            mpbase = 100 / mv3

            # The quote % move is the opposite of the base
            mpquote = mpbase * -1

        # update currency files adding the results and counting the number of results to calculate the average movement
        mcl = df3.loc[(df3.Date == mdate), 'RiseFall'] + mpbase
        df3.loc[(df3.Date == mdate), 'RiseFall'] = mcl
        mno = df3.loc[(df3.Date == mdate), 'No'] + 1
        df3.loc[(df3.Date == mdate), 'No'] = mno

        mcl = df4.loc[(df4.Date == mdate), 'RiseFall'] + mpquote
        df4.loc[(df4.Date == mdate), 'RiseFall'] = mcl
        mno = df4.loc[(df4.Date == mdate), 'No'] + 1
        df4.loc[(df4.Date == mdate), 'No'] = mno

        i2 = i2 + 1

    # Save currency files
    df3.drop(df3[df3['day_of_week'] == 'Sunday'].index, inplace=True)
    df3.to_csv('../csv/currency/' + mbase + '.csv', index=False)
    df4.to_csv('../csv/currency/' + mquote + '.csv', index=False)
    print(mtic + " Completed")
    i = i + 1
