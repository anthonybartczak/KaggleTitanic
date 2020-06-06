import pandas as pd
import numpy as np
import h2o as h
import os

for dirname, _, filenames in os.walk('input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

train_data = pd.read_csv("input/train.csv")
test_data = pd.read_csv("input/test.csv")
women = train_data.loc[train_data.Sex == 'female']["Survived"] # Filter women that survived.
men = train_data.loc[train_data.Sex == 'male']["Survived"] # Filter men that survived.

rate_men = sum(men)/len(men)
rate_women = sum(women)/len(women)

print("% of women who survived:", rate_women)
print("% of men who survived:", rate_men)