import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


borough = 'Manhattan'
filename = 'DataMining/cl4.csv'
plotStyle = 'Solarize_Light2'
numberRows = 12537000


"""
Plot many-violation streets for NY plates vs non-NY plates
"""


def getStreetPlateData(boroughName):

    # Get the dataframe and limit to the selected borough
    df = pd.read_csv(filename, usecols=['Street Name', 'Registration State', 'Violation County'], nrows=numberRows)
    df.fillna("")

    countyDF = df.loc[(df['Violation County'] == boroughName)]

    # Rename the states based on in state or out of state
    def cleanStates(state):
        if (state == 'NY'): return "In-state"
        else: return "Out-of-state"
    countyDF['Registration State'] = countyDF['Registration State'].apply(cleanStates)

    # Get the count based on state and street name, remove small values and sort by the count values
    countyDF = countyDF.groupby(['Registration State', 'Street Name']).count()
    countyDF.reset_index(inplace=True) # get state and street name as columns again
    countyDF = countyDF.loc[(countyDF['Violation County'] > 5)]
    countyDF = countyDF.sort_values('Violation County', ascending=False)

    # Get the five largest values for in-state and out-state
    maxIn = []
    countIn = []
    i = 0
    while (len(maxIn) < 5):
        row = countyDF.iloc[i]

        if row['Registration State'] == 'In-state':
            maxIn.append(row['Street Name'])
            countIn.append(row['Violation County'])

        i += 1

    maxOut = []
    countOut = []
    i = 0
    while (len(maxOut) < 5):
        row = countyDF.iloc[i]

        if row['Registration State'] != 'In-state':
            maxOut.append(row['Street Name'])
            countOut.append(row['Violation County'])

        i += 1

    ax1 = plt.subplot(2, 1, 1)
    plt.bar(maxIn, countIn)
    plt.title(boroughName + " Street Violations from In-State Plates")

    ax2 = plt.subplot(2, 1, 2, sharey=ax1)
    plt.bar(maxOut, countOut)
    plt.title(boroughName + " Street Violations from Out-of-State Plates")

    plt.xlabel('Street')
    plt.ylabel('Count')

    plt.style.use(plotStyle)
    plt.show()


"""
Get the violation count for the busiest street at every hour
"""


def getBusiestStreetsByHour(boroughName):

    df = pd.read_csv(filename, usecols=['Street Name', 'Violation Time', 'Violation County'], nrows=numberRows)
    df.fillna("")

    # select only those violations appearing in Manhattan
    countyDF = df.loc[(df['Violation County'] == boroughName)]

    # collapse times down to 1-hour intervals in military time
    def cleanTime(time):
        if time[-1] == 'P' and int(time[:2]) < 12:
            return int(time[:2]) + 12
        else:
            return int(time[:2])

    countyDF['Violation Time'] = countyDF['Violation Time'].apply(cleanTime)

    # get the streets with the max violation at every hour
    countyDF = countyDF.groupby(['Violation Time', 'Street Name']).count()
    countyDF.reset_index(inplace=True) # get violation time and street name as columns again
    countyDF = countyDF.groupby('Violation Time').max()
    countyDF.reset_index(inplace=True) # get the violation time as a column again

    # Plot / print the data
    print(countyDF['Street Name'])

    plt.barh(countyDF['Violation Time'], countyDF['Violation County'])
    plt.ylim(0, 25)

    plt.xlabel('Violation count')
    plt.ylabel('Time of day (military)')
    plt.title("Violations on busiest streets for every hour - " + boroughName)

    plt.style.use(plotStyle)
    plt.show()


"""
Get the busiest times for the busiest street
"""


def getBusyStreetTimes(boroughName):

    df = pd.read_csv(filename, usecols=['Street Name', 'Violation Time', 'Violation County'], nrows=numberRows)
    df.fillna("")

    # Get the rows with boroughName and West 14th St, group by count
    countyDF = df.loc[(df['Violation County'] == boroughName)]
    countyDF = countyDF.loc[(df['Street Name'] == 'WEST 14 ST')]
    countyDF = countyDF.groupby('Violation Time').count()

    amTimes = []
    pmTimes = []
    counts = []

    for index, row in countyDF.iterrows():
        if index[-1] == 'P' and int(index[:2]) < 12:
            hour = int(index[:2]) + 12
            pmTimes.append(hour)
        else:
            hour = int(index[:2])
            amTimes.append(hour)

        counts.append(row['Street Name'])

    times = amTimes + pmTimes

    plt.style.use(plotStyle)
    plt.barh(times, counts)

    plt.xlabel('Count')
    plt.ylabel('Time')
    plt.title('Time of Street Violations in ' + boroughName)

    plt.show()


"""
Get the busiest dates for the busiest street by borough
"""


def getStatenIslandBusyDates(amount):

    df = pd.read_csv(filename, usecols=['Street Name', 'Issue Date', 'Violation County'], nrows=numberRows)
    df.fillna("")

    countyDF = df.loc[(df['Violation County'] == 'Staten Island')]
    countyDF = countyDF.loc[(df['Street Name'] == 'NORTH GOETHALS RD')]
    countyDF = countyDF.groupby('Issue Date').count()

    dates = []
    counts = []
    for index, row in countyDF.iterrows():
        count = row['Street Name']
        if (count > amount):
            dates.append(index)
            counts.append(count)


    plt.style.use(plotStyle)
    plt.barh(dates, counts)

    plt.xlabel('Count')
    plt.ylabel('Date')
    plt.title('Date of Street Violations in Staten Island')

    plt.show()


def getManhattanBusyDates(amount):

    df = pd.read_csv(filename, usecols=['Street Name', 'Issue Date', 'Violation County'], nrows=numberRows)
    df.fillna("")

    countyDF = df.loc[(df['Violation County'] == 'Manhattan')]
    countyDF = countyDF.loc[(df['Street Name'] == 'WEST 14 ST')]
    countyDF = countyDF.groupby('Issue Date').count()

    dates = []
    counts = []
    for index, row in countyDF.iterrows():
        count = row['Street Name']
        if (count > amount):
            dates.append(index)
            counts.append(count)


    plt.style.use(plotStyle)
    plt.barh(dates, counts)

    plt.xlabel('Count')
    plt.ylabel('Date')
    plt.title('Date of Street Violations in Manhattan')

    plt.show()


getManhattanBusyDates(550)
"""
Get the streets with the most violations for each borough
"""


def getBusyStreets(boroughName, amount):

    df = pd.read_csv(filename, usecols=['Street Name','Violation County'], nrows=numberRows)
    df.fillna("")

    # Select for the appropriate county and group by street name
    countyDF = df.loc[df['Violation County'] == boroughName].groupby('Street Name').count()

    # Fill up two lists with names of streets and the corresponding count for that street
    streetNames = []
    counts = []
    for index, row in countyDF.iterrows():
        count = row['Violation County']
        if (count > amount):
            streetNames.append(index)
            counts.append(count)

    # Plot the data
    plt.style.use(plotStyle)
    plt.barh(streetNames, counts)

    plt.xlabel('Count')
    plt.ylabel('Street Name')
    plt.title('Count of Street Violations in ' + boroughName)

    plt.show()

