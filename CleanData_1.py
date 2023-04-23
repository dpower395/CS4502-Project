import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dask import dataframe as df1

df = pd.read_csv('parkingViolations2022.csv')

#converts Issue Date column to date format
df['Issue Date'] = pd.to_datetime(df['Issue Date'])

#removes commas so that no errors take place during string->int conversion
df = df.replace(',','', regex=True)

#converts strings to int for 'Vehicle Year' column
df = df.astype({'Vehicle Year':'int'})

#drop columns that have no values/are empty 
df = df.drop(columns=['Violation Post Code', 
    'Violation Description',
    'No Standing or Stopping Violation',
    'Hydrant Violation',
    'Double Parking Violation'])

#drop rows where:
#registration plate is invalid(dataset uses 99 for invalid entries )
#plate type is invalid (dataset uses 999 for invalid entries )
#violation code is (dataset uses the number 0 for invalid entries )
#vehicle make and violation times are empty
#vehicle year is invalid (0 or year is < 2022)


df= df[(df['Registration State'] != "99") 
    & (df['Plate Type'] != "999") 
    & (df['Violation Code'] != 0) 
    & (df['Vehicle Make'].notnull()) 
    & (df['Violation Time'].notnull()) 
    & (df['Vehicle Year'] != 0) 
    & (df['Vehicle Year'] <= 2022)]

pd.set_option('display.max_columns', None)
print('Number of Rows: ' + str(len(df)))
print(df.head(1))