import ScrapeTestingData
import ScrapeTrainingData
import DataCleanse

def main():
    # Scrape datasets
    training_data = ScrapeTrainingData.main()
    testing_data = ScrapeTestingData.main()

    # Season Stats for each team
    team_stats_dict = DataCleanse.getStatsDict('2022-23')   # Data we are testing is last year season data
    print(len(team_stats_dict))
    
if __name__ == "__main__":
    main()