import pandas as pd

from app.business import predictors
from app.models import Predictor
from app.models.Dataset import Dataset
from sklearn.model_selection import train_test_split


class ProcessingUtils:
    @staticmethod
    def get_expected_dataset_columns():
        return [
            'yield_um',
            'yield_ml',
            'calculated_mw',
            'calculated_pi',
            'sequence_length',
            'sequence_mass',
            'steric',
            'polarizability',
            'volume',
            'hydrophobicity',
            'helix',
            'sheet'
        ]

    @staticmethod
    def get_expected_dataset_prediction_columns():
        return [
            'solubility'
        ]

    @staticmethod
    def load_dataset(dataset: Dataset, prediction_property_key: str):
        raw_data = pd.read_csv(dataset.location.path)
        data = raw_data.copy()
        X = data[
            ProcessingUtils.get_expected_dataset_columns()
        ]
        y = data[[prediction_property_key]]

        X = round(X, 2)
        y = round(y, 2)

        return X, y

    @staticmethod
    def load_train_and_test_sets2(X, y, model: Predictor):
        prediction_property_key = predictors.get_prediction_type_by_key(model.prediction_type)
        sample_set = X.copy()
        sample_set[prediction_property_key] = y[prediction_property_key]

        sample_set = sample_set[
            [prediction_property_key] + [col for col in sample_set.columns if col != prediction_property_key]]
        train_split = 1.0 - float(model.split)
        seed = int(model.seed)
        train_dataset = sample_set.sample(frac=train_split, random_state=seed)
        test_dataset = sample_set.drop(train_dataset.index)

        return train_dataset, test_dataset

    @staticmethod
    def load_train_and_test_sets(X, y, model: Predictor):
        prediction_property_key = predictors.get_prediction_type_by_key(model.prediction_type)

        test_size = float(model.split)
        seed = int(model.seed)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

        training_set = X_train.copy()
        training_set[prediction_property_key] = y_train[prediction_property_key]
        training_set = training_set[
            [prediction_property_key] + [col for col in training_set.columns if col != prediction_property_key]]

        test_set = X_test.copy()
        test_set[prediction_property_key] = y_test[prediction_property_key]
        test_set = test_set[
            [prediction_property_key] + [col for col in test_set.columns if col != prediction_property_key]]

        return training_set, test_set

    @staticmethod
    def normalize(col_data):
        return (col_data - col_data.min()) / (col_data.max() - col_data.min())
