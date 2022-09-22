import pandas as pd

# update the relative strengths of the base and quote currencies in the comparison files

df = pd.read_csv('../csv/forex.csv')
rn = len(df)
i = 0
while i < rn:
    mtic = df.loc[i, 'ticker']

    # the first 3 characters are the base currency and 4th to 6th characters are the quote currency
    mbase = str(mtic)[0:3]
    mquote = str(mtic)[3:6]

    # using the 2 different currency files and the comparison file.
    df2 = pd.read_csv('../csv/working/' + mtic + '.csv')
    df3 = pd.read_csv('../csv/currency/' + mbase + '.csv')
    df4 = pd.read_csv('../csv/currency/' + mquote + '.csv')

    # Align indexes of currency files with ticker files (working directory)
    rn2 = len(df3)
    i2 = 0
    while i2 < rn2:
        mdate = df3.loc[i2, 'Date']
        if mdate in df2['Date'].values:
            pass
        else:
            df3 = df3.drop(df3[df3['Date'] == mdate].index)
        i2 = i2 + 1

    i2 = 0
    while i2 < rn2:
        mdate = df4.loc[i2, 'Date']
        if mdate in df2['Date'].values:
            pass
        else:
            df4 = df4.drop(df4[df4['Date'] == mdate].index)
        i2 = i2 + 1

    # save currency files as temporary files to keep the originals in tact
    df3 = df3.drop(df3[df3['RiseFall'] == 0].index)
    df3 = df3.loc[:, ~df3.columns.str.contains('^Unnamed')]
    df3.to_csv('../csv/working/t1.csv', index=False)

    df4 = df4.drop(df4[df4['RiseFall'] == 0].index)
    df4 = df4.loc[:, ~df4.columns.str.contains('^Unnamed')]
    df4.to_csv('../csv/working/t2.csv', index=False)

    df2.to_csv('../csv/working/t3.csv', index=False)

    df2 = pd.read_csv('../csv/working/t3.csv')
    df3 = pd.read_csv('../csv/working/t1.csv')
    df4 = pd.read_csv('../csv/working/t2.csv')

    # update ticker files in the working directory
    # with the relative currency strengths for base and quote
    i2 = 0
    rn2 = len(df2)
    while i2 < rn2:
        mdate = df2.loc[i2, 'Date']

        mb = df3.loc[(df3.Date == mdate), 'RiseFall']
        mbn = df3.loc[(df3.Date == mdate), 'No']
        mb = mb / mbn

        mq = df4.loc[(df4.Date == mdate), 'RiseFall']
        mqn = df4.loc[(df4.Date == mdate), 'No']
        mq = mq / mqn

        df2.loc[(df2.Date == mdate), 'Base'] = mb
        df2.loc[(df2.Date == mdate), 'Quote'] = mq
        i2 = i2 + 1

    # Save updated ticker files
    df2.to_csv('../csv/working/' + mtic + '.csv', index=False)
    print(mtic + "Updated")
    i = i + 1
