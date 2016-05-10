#!/usr/bin/python

import csv, os, sys
import numpy as np
import pandas as pd

# Building query to fetch data from API
apiBase = "http://api.worldbank.org/indicator/"
apiIndicator = "SI.POV.GINI"    # This can be changed to any other indicator
FILE_NAME = 'gini-index.csv'
source = apiBase+apiIndicator+"?format=csv"
print(source)

def main():
    giniIndex = pd.read_csv(source)
    giniIndex.to_csv('archive/gini-index.csv', sep=",", index_col=0, index=False) 
    print("Saved archive CSV file.")
    print (giniIndex)
    
    # Processing the data
    df = pd.read_csv('archive/gini-index.csv')      # Reading the source csv
    """
    Python is printing "Country Name" with quotes in data frame and does not
    work for the remaining code
    """
    df.columns.values[0] = 'Country Name'
    
    df = pd.melt(df, id_vars=['Country Name', 'Country Code'], var_name="Year", value_name="Value")     # Unpivoting
    df = df.sort_values(by=['Country Name', 'Year'], ascending=[True, True]) # Sorting by country

    df.dropna().to_csv('data/gini-index.csv', sep=",", index=False)   # Saving CSV
    print ("File has been saved and it is ready for data packaging.")

if __name__ == "__main__":
    main()
