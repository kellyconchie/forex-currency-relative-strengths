import pandas as pd
from datetime import date
from datetime import timedelta
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt

# Main plots are the last 200 days
x2 = 200
# The magnified plot is the last 30 days
x = 30

# declare variables for short and long term directions
short = " "
long = " "

# Using the date time library get start and end dates to plot
# ts start day 30 days previous
# ts2 start day 200 days previous

today = date.today()
start = today - timedelta(x)
td = str(today)
ts = str(start)

ts2 = x2
star = today - timedelta(ts2)
ts2 = str(star)


# Graph function
def plotone():
    # Dates to plot
    newtime = df[df['Date'].between(ts, td)]
    newtime2 = df[df['Date'].between(ts2, td)]

    fig = plt.figure()
    fig.suptitle(name2, fontsize=16)

    # setup grid to display 3 plots
    gs = GridSpec(2, 2)  # 2 rows, 2 columns

    ax1 = fig.add_subplot(gs[0, 0])  # First row, first column
    ax1.plot(newtime[['Close', 'High', 'Low']])
    plt.title("Last 30 days since " + ts)
    ax1.legend(['Close', 'High', 'Low'])

    ax2 = fig.add_subplot(gs[0, 1])  # First row, second column
    ax2.plot(newtime2[['Quote', 'Base']])
    plt.title("200 days currency relative strength since " + ts2)
    ax2.legend([mquote, mbase])

    ax3 = fig.add_subplot(gs[1, :])  # Second row, span all columns
    ax3.plot(newtime2[['Close', 'Av5', 'Av10', 'Av30']])
    ax3.legend(['Close', 'Av5', 'Av10', 'Av30'])
    plt.title("200 days since " + ts2)

    # Display full screen
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()


# Scan all comparison files for comparisons to graph
dff = pd.read_csv('../csv/forex.csv')
dff = dff.reset_index()
rn = len(dff)
di = 0
mcount = 1

while di < rn:
    ticker = dff.loc[di, 'ticker']
    mbase = str(ticker)[0:3]
    mquote = str(ticker)[3:6]
    name = dff.loc[di, 'currency']
    df = pd.read_csv("../csv/working/" + ticker + ".csv")

    print(ticker)

    # Algorithm to determine which currency comparisons to display. In this case when the 5 day moving average
    # crosses the 10 day moving average in either direction
    last = len(df) - 1
    if df.loc[last, 'Av5'] <= df.loc[last, 'Av10'] and df.loc[last - 1, 'Av5'] >= df.loc[last - 1, 'Av10'] or df.loc[
        last, 'Av5'] >= df.loc[last, 'Av10'] and df.loc[last - 1, 'Av5'] <= df.loc[last - 1, 'Av10']:

        # if the 5 day average today is greater than the 5 day average yesterday then the short term direction is up
        # else it is down
        if df.loc[last, 'Av5'] >= df.loc[last - 1, 'Av5']:
            print(df.loc[last - 1, 'Av5'])
            print(df.loc[last, 'Av5'])
            short = "UP"
            print(short)
        else:
            short = "DOWN"
            print(df.loc[last - 1, 'Av5'])
            print(df.loc[last, 'Av5'])
            print(short)

        # if the 30 day average today is greater than the 30 day average of yesterday then the long term direction is
        # up else it is down
        if df.loc[last, 'Av30'] >= df.loc[last - 1, 'Av30']:
            long = "UP"
            print(df.loc[last - 1, 'Av30'])
            print(df.loc[last, 'Av30'])
            print(long)
        else:
            long = "DOWN"
            print(df.loc[last - 1, 'Av30'])
            print(df.loc[last, 'Av30'])
            print(long)

        # if statement to either show a comparison or skip to next.
        ans = input("Do you want to graph " + name + " Y/N")
        if ans == "Y" or ans == "y":
            name2 = ticker + " " + name + "\n Long term direction is " + long + "\n Short term direction is " + short
            plotone()

    di = di + 1
