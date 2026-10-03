import kagglehub
import pandas as pd
import os

# Download latest version
path = kagglehub.competition_download('playground-series-s6e10')

print("Path to competition files:", path)
path = "/Users/dingg/.cache/kagglehub/competitions/playground-series-s6e10"



train = pd.read_csv(os.path.join(path, "train.csv"))
test = pd.read_csv(os.path.join(path, "test.csv"))
sample = pd.read_csv(os.path.join(path, "sample_submission.csv"))

train.head()

train.describe()
