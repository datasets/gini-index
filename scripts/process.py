#!/usr/bin/python

import os, csv
import requests
import zipfile
import tempfile
import pandas as pd

tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
tmpdir = tempfile.TemporaryDirectory()

API_INDICATOR = "SI.POV.GINI"
SOURCE_URL = f"https://api.worldbank.org/v2/en/indicator/{API_INDICATOR}?downloadformat=csv"
ARCHIVE_FILE = 'archive/gini-index.csv'
OUTPUT_FILE = 'data/gini-index.csv'

def download_zip_file():
    response = requests.get(SOURCE_URL)
    
    with open(tmpfile.name, 'wb') as d:
        d.write(response.content)
    
    with zipfile.ZipFile(tmpfile.name, 'r') as zip_ref:
        zip_ref.extractall(tmpdir.name)
    
    os.unlink(tmpfile.name)
    
    for path in os.scandir(tmpdir.name):
        if path.is_file() and 'metadata' not in path.name.lower():
            filename = os.path.join(tmpdir.name, path.name)
            archive_path = os.path.join('archive', 'gini-index.csv')
            
            # Ensure the archive folder exists
            os.makedirs('archive', exist_ok=True)
            
            os.rename(filename, archive_path)
            print(f"File saved to: {archive_path}")

def process_population_data(filename, output_file):
    # Read the raw CSV file
    with open(filename) as fo:
        lines = [row for row in csv.reader(fo)]
    
    # Extract headings and data rows
    headings = lines[4]
    lines = lines[5:]
    
    # Define output structure
    outheadings = ['Country Name', 'Country Code', 'Year', 'Value']
    outlines = []

    # Process each row and reshape the data
    for row in lines:
        for idx, year in enumerate(headings[4:]):
            if row[idx + 4]:  # Check if the value exists
                value = row[idx + 4]
                outlines.append(row[:2] + [int(year), value])

    df = pd.DataFrame(outlines, columns=outheadings)
    
    df = df.sort_values(by=['Country Name', 'Year'])
    df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")

# Example usage
if __name__ == "__main__":
    download_zip_file()
    process_population_data(ARCHIVE_FILE, OUTPUT_FILE)

