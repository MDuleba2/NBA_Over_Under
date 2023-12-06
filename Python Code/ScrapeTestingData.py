import pandas as pd
import os

def main():
    # Retrieve files and folders
    folder_location = r'Testing Data'

    # Store columns
    columns = ['Away', 'Home', 'Result']
    testing_data = pd.DataFrame()

    # Loop through each file in directory
    for file in os.listdir(folder_location):
        # Store file location
        file_location = folder_location + '/' + file

        # Read in data
        data = pd.read_csv(file_location)
        
        # Adjust columns
        data = data[['Visitor/Neutral', 'Home/Neutral']]
        data['Result'] = ''
        data.columns = columns

        # Append dataframe
        testing_data = pd.concat([testing_data, data], ignore_index=True)

    return testing_data