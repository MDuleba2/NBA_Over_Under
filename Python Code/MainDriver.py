import ScrapeTestingData
import ScrapeTrainingData
import DataCleanse
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler



def modelPrediction(team_stats_df, training_data, testing_data):
    ''' 
    This method takes in all of the data that we have extracted
    and creates usable data so that we can predict the winner
    of the given testing set. 

    @param team_stats_df: all team stats
    @param training_data: data used to train the model
    @param testing_data: data used to test the model
    @return predictions
    '''

    # Prepare training combined stats
    training_combined_stats = []
    for _, row in training_data.iterrows():
        away_team_stats = team_stats_df.loc[row['Away']]
        home_team_stats = team_stats_df.loc[row['Home']]
        combined_stats = pd.concat([away_team_stats, home_team_stats], axis=0).values.flatten()
        training_combined_stats.append(combined_stats)

    # Extract winners as target labels for training
    y_train = training_data['Result']

    # Prepare testing combined stats
    testing_combined_stats = []
    for _, row in testing_data.iterrows():
        away_team_stats = team_stats_df.loc[row['Away']]
        home_team_stats = team_stats_df.loc[row['Home']]
        combined_stats = pd.concat([away_team_stats, home_team_stats], axis=0).values.flatten()
        testing_combined_stats.append(combined_stats)

    # Scale the dataset
    scaler = StandardScaler()
    scaled_training_combined_stats = scaler.fit_transform(training_combined_stats)
    scaled_testing_combined_stats = scaler.transform(testing_combined_stats)

    # Train a Logistic Regression model
    model = LogisticRegression(max_iter=2000)
    model.fit(scaled_training_combined_stats, y_train)
    predictions = model.predict(scaled_testing_combined_stats)

    return predictions

def main():

    # Season Stats for each team
    team_stats_df = DataCleanse.getTeamStats('2022-23')   # Data we are testing is last year season data
    
    # Scrape datasets
    training_data = ScrapeTrainingData.main()
    testing_data = ScrapeTestingData.main()

    # Get predicitons for our model
    predictions = modelPrediction(team_stats_df, training_data, testing_data)
    print(predictions)

    # Calculate accuracy


if __name__ == "__main__":
    main()