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

train.info()
train.describe()

# Hypothesis inflight wifi service affects satisfaction
nowifi = train[train["Inflight wifi service"] == 0]
yeswifi = train[train["Inflight wifi service"] != 0]
print(nowifi.shape)
print(yeswifi.shape)
print(nowifi["satisfaction"].value_counts())
print(yeswifi["satisfaction"].value_counts())

wifi_stats = train.groupby("Inflight wifi service")["satisfaction"].agg(["mean", "count"])
print(wifi_stats)