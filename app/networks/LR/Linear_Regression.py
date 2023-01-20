import pandas as pd
from tensorflow import keras, sqrt
#from sklearn.linear_model import LinearRegression
from app.networks.shared.BaseNetwork import BaseNetwork
from sklearn import metrics
import matplotlib as plt


import tensorflow as tf

class RF(BaseNetwork):

    # Construct the keras sequential model used for the activation function (ReLu)
    def compile(self):
        if self.model:
            raise Exception("Model has already been compiled")

        self.model = tf.keras.Sequential([
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(1)
        ])

        # Normalise the model to be trained
        self.model = tf.keras.layers.Normalization().adapt(self.model)

        #self.model = LinearRegression().fit(X,y,sample_weight=None)
        #return self.model

        # Compile the model
        self.model.compile(
            # Compile the loss and the optimizer arguments
            loss=tf.keras.metrics.MeanAbsoluteError(name='MAE'),
            optimizer=tf.keras.optimizers.Adam(float(self.predictor.learning_rate)),

        )
        return self.model

    def train(self):
        trained_model = self.model.fit(
            self.train_features,
            self.train_labels,
            # Define the epochs on which the model is executed
            epochs=200,
            # Suppress all logging
            verbose=0,
            # Compute the validation of the results on X% of the training data.
            # validation_split= X.X

        )

        # Represent the model in a histogram diagram.
        hist = pd.DataFrame(trained_model.trained_model)
        hist['epoch'] = trained_model.epoch
        hist.tail()

        plt.plot(trained_model.trained_model['loss'], label='loss')
        plt.plot(trained_model.trained_model['val_loss'], label='val_loss')
        plt.ylim([0, 10])
        plt.xlabel('Epoch')
        plt.ylabel('Error [MPG]')
        plt.legend()
        plt.grid(True)

    # Collect the test results
    def test(self):
        self.results = []
        results = self.results
        results[self.model] = self.model.evaluate(
            self.test_features,
            self.test_labels, verbose=0
        )

         # Predict the features
        predictions = self.model.predict(self.test_features)
        results.append(sqrt(metrics.mean_squared_error(self.test_labels, predictions)))
        results.append(metrics.mean_absolute_error(self.test_labels, predictions))

        return self.results

     # def plot_model(x,y):
     #     x = tf.linspace(0.0, 250, 251)
     #     plt.scatter(test(train_features), self.train_labels, label='Data')
     #     plt.plot(x, y, color='k', label='Predictions')
     #     plt.xlabel('Data labels')
     #     plt.ylabel('MPG')
     #     plt.legend()

