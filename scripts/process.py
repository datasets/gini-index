#!/usr/bin/python

import csv, os
import numpy as np
import pandas as pd

# importing the sheet as a dataframe        # Must change directory to file path
os.chdir('/gini-index/data/')    # no need to leave yours here

def main():
    df = pd.read_csv("gini-index.csv")      # Reading the source csv
    df = pd.melt(df, id_vars=['Country Name', 'Country Code'], var_name="Year", value_name="Vaue")     # Unpivoting
    df = df.sort_values(['Country Name']) # Sorting by country

    df.dropna().to_csv('gini-index.csv', sep=",", index=False)   # Saving CSV



if __name__ == '__main__':
    main()
