import pandas as pd
import numpy as np
import os
from h2o.estimators import H2ORandomForestEstimator
import h2o

h2o.init()

train_data = h2o.import_file(path="input/train.csv", na_strings=[""])
test_data = h2o.import_file(path="input/test.csv", na_strings=[""])

training_columns = ["Pclass", "Sex", "SibSp", "Parch"]
response_column = "Survived"

model = H2ORandomForestEstimator(ntrees=100, max_depth=5)
model.train(x=training_columns, y=response_column, training_frame=train_data)
predictions = model.predict(test_data)

test_data = test_data.as_data_frame()
predictions = predictions.as_data_frame()
output = pd.DataFrame({'PassengerId': test_data.PassengerId, 'Survived': predictions})
output.to_csv('my_submission.csv', index=False)