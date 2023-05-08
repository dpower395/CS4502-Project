import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('parkingViolations2022_Cleaned.csv')

pd.set_option('display.max_columns', None)

#Top 10 violation codes for vehicles that are registered in NY
#Groups by violation code and by using the unique sommons number 
print(df[df['Registration State'] == 'NY'].groupby('Violation Code')['Summons Number'].count().nlargest(10).reset_index(name='Count'))

#dataset based on above dataframe 
data = {'36':3727641, 
        '21':1080825, 
        '38':774299,
        '71':650015, 
        '14':595007,
        '20':521582,
        '5':517040,
        '40':473992,
        '7':462638,
        '70':361270,
}
codes = list(data.keys())
values = list(data.values())
  
fig = plt.figure(figsize = (10, 5))
 
plt.bar(codes, values, color ='blue',
        width = 0.4)
 
plt.xlabel("Violation Code")
plt.ylabel("Number of Violations (millions)")
plt.title("Most Common Violation Codes for Vehicles Registered In NY")
plt.show()


#Top 10 violation codes for vehicles that are registered in outside states of New York 
print(df[df['Registration State'] != 'NY'].groupby('Violation Code')['Summons Number'].count().nlargest(10).reset_index(name='Count'))

#dataset based on above dataframe 
data = {'36':955094, 
        '5':161412, 
        '7':126441,
        '12':11480, 
        '40':8717,
        '98':5817,
        '21':4242,
        '46':3696,
        '14':2826,
        '74':1777,
}
codes = list(data.keys())
values = list(data.values())
  
fig = plt.figure(figsize = (10, 5))
 
plt.bar(codes, values, color ='green',
        width = 0.4)
 
plt.xlabel("Violation Code")
plt.ylabel("Number of Violations (millions)")
plt.title("Most Common Violation Codes for Vehicles Registered Outside of NY")
plt.show()

#Most common violation codes for passenger vehicle types
print(df[df['Plate Type'] == 'PAS'].groupby('Violation Code')['Summons Number'].count().nlargest(1).reset_index(name='Count'))

#Most common violation codes for commerical vehicle types 
print(df[df['Plate Type'] == 'COM'].groupby('Violation Code')['Summons Number'].count().nlargest(1).reset_index(name='Count'))