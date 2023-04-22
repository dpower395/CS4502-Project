import numpy as np
import pandas as pd
import re

"""
README:
This file contains one function for standardizing county names, and another for street names
To use, add an 'import CleanData' statement to the top of another file
Pass in the data by calling CleanData.cleanTheStreets(df), and the function will create a new csv for you

Right now, the functions assumes NaN values have been changed to an empty string
(You can change the NaN values to "" with df.fillna(""))

You'll also probably get a warning about setting on a copy but it's fine
"""

"""
Todo:
There are airport violations with things like:
'terminal 5', 't5', 'jfk', 'departures', still need to deal with these

Additionally, this function doesn't account for typos/duplicates in the 'street names' column yet
Still need to handle 'of', 'and', and '@' in the names too
"""

def cleanTheStreets(dFrame):

    # N E S W
    north = re.compile(r'(\s|^)n(\s|$)|north(\s|$)', re.IGNORECASE) # checks for n, north, NORTH, etc
    east = re.compile(r'(\s|^)e(\s|$)|east(\s|$)', re.IGNORECASE)
    south = re.compile(r'(\s|^)s(\s|$)|south(\s|$)', re.IGNORECASE)
    west = re.compile(r'(\s|^)w(\s|$)|west(\s|$)', re.IGNORECASE)

    directionMap = {
        north: "NORTH ",
        east: "EAST ",
        south: "SOUTH ",
        west: "WEST "
    }

    # Ave / St, etc
    ave = re.compile(r'(\s|^)av(\s|$)|(\s|^)ave(\s|$)|avenue', re.IGNORECASE) # checks for av, ave, etc
    st = re.compile(r'(\s|^)st(\s|$)|(\s|^)street(\s|$)', re.IGNORECASE)
    rd = re.compile(r'(\s|^)rd(\s|$)|(\s|^)road(\s|$)', re.IGNORECASE)
    blvd = re.compile(r'blvd|boulevard', re.IGNORECASE)
    pl = re.compile(r'(\s|^)pl(\s|$)|(\s|^)place(\s|$)', re.IGNORECASE)
    drive = re.compile(r'(\s|^)dr(\s|$)|(\s|^)drive(\s|$)', re.IGNORECASE)
    walk = re.compile(r'(\s|^)walk(\s|$)', re.IGNORECASE)
    br = re.compile(r'(\s|^)br(\s|$)|(\s|^)branch(\s|$)', re.IGNORECASE)

    typeMap = {
        ave: "AVE",
        st: "ST",
        rd: "RD",
        blvd: "BLVD",
        pl: "PL",
        drive: "DRIVE",
        walk: "WALK",
        br: "BRANCH"
    }

    # Name
    name = re.compile(r'(\s|^)[a-z]{3,}(\s|$)', re.IGNORECASE) # checks for actual street names

    # Number
    num = re.compile(r'[0-9]+') # checks for numbers


    for index, row in dFrame.iterrows():

        curVal = row['Street Name'].lower()
        origVal = curVal
        
        # Find out if any N E S W parts are in the name
        direction = ""
        for key in directionMap:
            match = key.search(curVal)

            if (match):
                direction = directionMap[key]
                (start, stop) = match.span()
                curVal = curVal[ : start] + " " + curVal[stop : ]
                break
        
        # Find words like ave, street
        type = ""
        for key in typeMap:
            match = key.search(curVal)

            if (match):
                type = typeMap[key]
                (start, stop) = match.span()
                curVal = curVal[ : start] + " " + curVal[stop : ]
                break
        
        # Find street number
        number = ""
        match = num.search(curVal)

        if (match):
            number = match.group() + " "
            (start, stop) = match.span()
            curVal = curVal[ : start] + " " + curVal[stop : ]

        # Get the name of the street, maybe two words
        thisName = ""
        match = name.search(curVal)

        if (match):
            thisName = match.group().strip().upper() + " "
            (start, stop) = match.span()
            curVal = curVal[ : start] + " " + curVal[stop : ]

        thisName2 = ""
        match = name.search(curVal)

        if (match):
            thisName2 = match.group().strip().upper() + " "
            (start, stop) = match.span()
            curVal = curVal[ : start] + " " + curVal[stop : ]


        # create the new standardized name
        newVal = direction + number + thisName + thisName2 + type
        newVal = newVal.strip()

        # set the new name
        dFrame['Street Name'][index] = newVal

    # save to new csv
    dFrame.to_csv('modifiedStreet.csv', index=False)



countyMap = {
    "": 'NaN',

    "BX": "Bronx",
    "Bronx": "Bronx",

    "Q": "Queens",
    "QN": "Queens",
    "Qns": "Queens",

    "K": "Brooklyn",
    "BK": "Brooklyn",
    "Kings": "Brooklyn",

    "NY": "Manhattan",
    "MN": "Manhattan",

    "R": "Staten Island",
    "Rich": "Staten Island",
    "ST": "Staten Island",
    "RICH": "Staten Island"
}

def cleanTheCounties(dFrame):
    for index, row in dFrame.iterrows():
        curVal = row['Violation County']
        newVal = countyMap[curVal]
        dFrame['Violation County'][index] = newVal
    
    dFrame.to_csv('modifiedcounty.csv', index=False)