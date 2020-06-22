from h2o.estimators import H2ORandomForestEstimator
from h2o import H2OFrame
import h2o
import os
import pandas as pd

class ForestInitializer(object):

    def __init__(self):
        #Add default model values
        self.seed = 1
        self.ntrees = 100 # Suggested 100
        self.max_depth = 1000 # Suggested 1000

    def initForest(self):
        
        h2o.init()

        train_data = h2o.import_file("input/train.csv")
        test_data = h2o.import_file("input/test.csv")
        
        #train_data = train_data.fillna(axis=0, method='forward', maxlen=100)

        # Replacing missing age with avg age
        train_data[train_data["Age"].isna(), "Age"] = 29

        # Dropping it as it's not relevant now
        train_data = train_data.drop('PassengerId')

        training_columns = train_data.columns
        response_column = "Survived"
        train_data[response_column] = train_data[response_column].asfactor()

        train_data, valid_data = train_data.split_frame(ratios=[.5])

        model = H2ORandomForestEstimator(
            seed=self.seed,
            ntrees=self.ntrees,
            max_depth=self.max_depth,
            score_each_iteration=True)

        model.train(
            x=training_columns,
            y=response_column,
            training_frame=train_data,
            validation_frame=valid_data)

        predictions = model.predict(test_data)
        predictions = predictions[0].as_data_frame().values.flatten()

        train_data.summary()

        sample_submission = pd.read_csv('input/gender_submission.csv')
        sample_submission['Survived'] = predictions
        sample_submission.to_csv('output/titanic_h2o.csv', index=False)
        performance = model.model_performance(train_data, test_data)
        performance
        
        acc = performance.accuracy()
        logl = performance.logloss()
        auc = performance.auc()

        return acc, logl, auc

        # Check AUC for performance (increase is better)
        # Check LogLoss for performance (decrease is better)