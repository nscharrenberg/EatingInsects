import pandas as pd

from app.models import Predictor
from app.models.Dataset import Dataset


class ProcessingUtils:
    @staticmethod
    def load_dataset(dataset: Dataset):
        raw_data = pd.read_csv(dataset.location.path)
        data = raw_data.copy()
        X = data[['Yield(uM)','Yield(ug/ml)','Calculated MW(kDa)','Calculated pI', 'Sequence length', 'Sequence mass']]
        y = data.iloc[:, 1:2]

        # for column in X:
        #     X[column] = ProcessingUtils.normalize(X[column])

        X = round(X, 2)
        # y = round(ProcessingUtils.normalize(y), 2)
        y = round(y, 2)

        return X, y

    @staticmethod
    def load_train_and_test_sets(X, y, model : Predictor):
        sample_set = X.copy()
        sample_set['Solubility(%)'] = y['Solubility(%)']

        sample_set = sample_set[['Solubility(%)'] + [col for col in sample_set.columns if col != 'Solubility(%)']]
        train_split = 1.0 - float(model.split)
        seed = int(model.seed)
        train_dataset = sample_set.sample(frac=train_split, random_state=seed)
        test_dataset = sample_set.drop(train_dataset.index)

        return train_dataset, test_dataset

    @staticmethod
    def normalize(col_data):
        return (col_data - col_data.min()) / (col_data.max() - col_data.min())

