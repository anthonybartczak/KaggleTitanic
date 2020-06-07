import pandas as pd
import numpy as np
import os
from h2o.estimators import H2ORandomForestEstimator
import h2o

h2o.init()

train_data = h2o.import_file("input/train.csv")
test_data = h2o.import_file("input/test.csv")

training_columns = train_data.columns
response_column = "Survived"
train_data[response_column] = train_data[response_column].asfactor()

print(train_data)

model = H2ORandomForestEstimator(
    ntrees=2000,
    max_depth=10,
    score_each_iteration=True)

model.train(x=training_columns, y=response_column, training_frame=train_data)

predictions = model.predict(test_data)
predictions = predictions[0].as_data_frame().values.flatten()

sample_submission = pd.read_csv('input/gender_submission.csv')
sample_submission['Survived'] = predictions
sample_submission.to_csv('output/titanic_h2o.csv', index=False)

print(model.model_performance(train_data, test_data))