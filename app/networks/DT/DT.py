from math import sqrt

from sklearn.tree import DecisionTreeRegressor
from sklearn import metrics
from app.networks.shared.BaseNetwork import BaseNetwork


class DT(BaseNetwork):
    def compile(self):
        if self.model:
            raise Exception("Model has already been compiled")

        self.model = DecisionTreeRegressor(random_state=0, min_samples_leaf=15)

        return self.model

    def train(self):
        self.model.fit(
            self.train_features,
            self.train_labels,
        )

    def test(self):
        predictions = self.model.predict(self.test_features)
        self.results = []
        self.results.append(sqrt(metrics.mean_squared_error(self.test_labels, predictions)))
        self.results.append(metrics.mean_absolute_error(self.test_labels, predictions))

        return self.results
