import pandas as pd

from app.business import predictors
from app.models import Predictor
from app.models.Dataset import Dataset


class ProcessingUtils:
    @staticmethod
    def load_dataset(dataset: Dataset, prediction_property_key: str):
        raw_data = pd.read_csv(dataset.location.path)
        data = raw_data.copy()
        X = data[
            [
                'Yield(uM)',
                'Yield(ug/ml)',
                'Calculated MW(kDa)',
                'Calculated pI',
                'Sequence length',
                'Sequence mass',
                'Steric parameter',
                'Polarizability',
                'Volume',
                'Hydrophobicity',
                'Helix probability',
                'Sheet probability'
            ]
        ]
        y = data[[prediction_property_key]]

        X = round(X, 2)
        y = round(y, 2)

        return X, y

    @staticmethod
    def load_train_and_test_sets(X, y, model: Predictor):
        prediction_property_key = predictors.get_prediction_type_by_key(model.prediction_type)
        sample_set = X.copy()
        sample_set[prediction_property_key] = y[prediction_property_key]

        sample_set = sample_set[[prediction_property_key] + [col for col in sample_set.columns if col != prediction_property_key]]
        train_split = 1.0 - float(model.split)
        seed = int(model.seed)
        train_dataset = sample_set.sample(frac=train_split, random_state=seed)
        test_dataset = sample_set.drop(train_dataset.index)

        return train_dataset, test_dataset

    @staticmethod
    def normalize(col_data):
        return (col_data - col_data.min()) / (col_data.max() - col_data.min())
