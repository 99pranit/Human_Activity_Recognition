import pandas as pd
import os
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_colwidth', None)  # Show full content in each cell
pd.set_option('display.width', 1000)  # Set max width

dataset_path = os.getcwd().replace('/notebook' , '') + "/dataset/"

walking_df = pd.read_csv(dataset_path + "walking.csv")
downstairs_df = pd.read_csv(dataset_path + "downstairs.csv")
upstairs_df = pd.read_csv(dataset_path + "upstairs.csv")
sitting_df = pd.read_csv(dataset_path + "sitting.csv")
jogging_df = pd.read_csv(dataset_path + "jogging.csv")
standing_df = pd.read_csv(dataset_path + "standing.csv")
sleeping_df = pd.read_csv(dataset_path + "sleeping.csv")

walking_df['Target'] = 0
jogging_df['Target'] = 1
downstairs_df['Target'] = 2
upstairs_df['Target'] = 3
sitting_df['Target'] = 4
standing_df['Target'] = 5
sleeping_df['Target'] = 6

test_df  = pd.concat([walking_df , downstairs_df , upstairs_df , sitting_df , jogging_df , standing_df , sleeping_df] , axis=0)

test_df.columns = test_df.columns.str.replace("'", '')
test_df.to_csv('imu_data.csv')
