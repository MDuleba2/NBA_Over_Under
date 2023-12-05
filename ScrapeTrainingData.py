import openpyxl
import pandas as pd
import os

# Retrieve files and folders
folder_location = r'Training Data'

columns = ['Away', 'Home', 'Result (Winner)']
training_data = pd.DataFrame()

for file in os.listdir(folder_location):
    file_location = folder_location + '/' + file

    # Read in data
    data = pd.read_csv(file_location)
    data = data.iloc[:, 2:6]

    # Add Result column
    data['Result'] = data.apply(lambda row: row['Visitor/Neutral'] if row['Visitor PTS'] > row['Home PTS']
                         else row['Home/Neutral'] if row['Home PTS'] > row['Visitor PTS']
                         else 'Visitor/Neutral', axis=1)    
    
    training_data = pd.concat([training_data, data], ignore_index=True)

# Drop columns
drop_columns = ['Visitor PTS', 'Home PTS']
training_data.drop(columns=drop_columns, inplace=True)
training_data = training_data.rename(columns={'Visitor/Neutral': 'Away', 'Home/Neutral': 'Home', 'Result': 'Result'})

print(training_data)