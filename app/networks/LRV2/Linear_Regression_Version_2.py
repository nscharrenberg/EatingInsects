from numpy import sqrt
from sklearn.linear_model import LinearRegression
from app.networks.shared.BaseNetwork import BaseNetwork
from sklearn import metrics


class LRV2(BaseNetwork):

    # Construct the keras sequential model used for the activation function (ReLu)
    def compile(self):
        if self.model:
            raise Exception("Model has already been compiled")

        self.model = LinearRegression()

        return self.model

    def train(self):
        self.model.fit(
            self.train_features,
            self.train_labels,
        )

    # Collect the test results
    def test(self):
        self.results = []

        #results = self.model.evaluate(self.test_features, self.test_labels, verbose=0)
        # Predict the features
        predictions = self.model.predict(self.test_features)
        self.results.append(sqrt(metrics.mean_squared_error(self.test_labels, predictions)))
        self.results.append(metrics.mean_absolute_error(self.test_labels, predictions))

        return self.results
