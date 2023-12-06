import pandas as pd
import os

def main():
    # Retrieve files and folders
    folder_location = r'Testing Data'

    # Store columns
    columns = ['Away', 'Home', 'Result']
    testing_data = pd.DataFrame()
    testing_data_results = pd.DataFrame()
    result = []

    # Loop through each file in directory
    for file in os.listdir(folder_location):
        # Store file location
        file_location = folder_location + '/' + file

        # Read in data
        data = pd.read_csv(file_location)
        
        # Adjust columns
        data = data.iloc[:, 2:6]
        data['Result'] = ''

        # Add Result column
        result = data.apply(lambda row: row['Visitor/Neutral'] if row['Visitor PTS'] > row['Home PTS']
                            else row['Home/Neutral'] if row['Home PTS'] > row['Visitor PTS']
                            else 'Visitor/Neutral', axis=1)

        # Append dataframe
        testing_data = pd.concat([testing_data, data], ignore_index=True)

    # Drop columns
    drop_columns = ['Visitor PTS', 'Home PTS']
    testing_data.drop(columns=drop_columns, inplace=True)
    testing_data = testing_data.rename(columns={'Visitor/Neutral': 'Away', 'Home/Neutral': 'Home', 'Result': 'Result'})

    return testing_data, result