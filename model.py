import pandas as pd
import numpy as np
import os
from h2o.estimators import H2ORandomForestEstimator
import h2o

class ForestInitializer(object):

    def __init__(self):
        #Add default model values
        self.seed = 1
        self.ntrees = 500 # Add this to parameter selection.
        self.max_depth = 20 #suggested 1000

    def initForest(self):
        
        h2o.shutdown()
        h2o.init(
            nthreads=-1
        )

        train_data = h2o.import_file("input/train.csv")
        test_data = h2o.import_file("input/test.csv")

        train_summary = train_data.summary(return_data=True)
        test_summary = test_data.summary(return_data=True)

        # Dropping it as 
        train_data = train_data.drop('PassengerId')

        training_columns = train_data.columns
        response_column = "Survived"
        train_data[response_column] = train_data[response_column].asfactor()

        model = H2ORandomForestEstimator(
            seed=self.seed,
            ntrees=self.ntrees,
            max_depth=self.max_depth,
            score_each_iteration=True)

        model.train(
            x=training_columns,
            y=response_column,
            training_frame=train_data)

        predictions = model.predict(test_data)
        predictions = predictions[0].as_data_frame().values.flatten()

        sample_submission = pd.read_csv('input/gender_submission.csv')
        sample_submission['Survived'] = predictions
        sample_submission.to_csv('output/titanic_h2o.csv', index=False)

        print(model.model_performance(train_data, test_data))

        # Check AUC for performance (increase is better)
        # Check LogLoss for performance (decrease is better)