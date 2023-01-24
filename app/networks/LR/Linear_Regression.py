from tensorflow import keras, sqrt
from app.networks.shared.BaseNetwork import BaseNetwork
from sklearn import metrics
import tensorflow as tf

class LR(BaseNetwork):

    # Construct the keras sequential model used for the activation function (ReLu)
    def compile(self):
        if self.model:
            raise Exception("Model has already been compiled")

        # Adapt the model to be trained WITHOUT normalization
        self.model = tf.keras.Sequential([
            keras.layers.Dense(1, activation='linear')
        ])

        # Adapt the model to be trained WITHOUT normalization
        #self.model = tf.keras.layers.(self.model)

        #self.model = LinearRegression().fit(X,y,sample_weight=None)
        #return self.model

        # Compile the model
        self.model.compile(
            # Compile the loss and the optimizer arguments
            loss=keras.metrics.RootMeanSquaredError(name="RMSE"),
            optimizer=keras.optimizers.Adam(float(self.predictor.learning_rate)),
            metrics=[keras.metrics.MeanAbsoluteError(name="MAE")]
        )
        return self.model

    def train(self):
        self.model.fit(
            self.train_features,
            self.train_labels,
            # Define the batch size.
            batch_size=128,
            # Define the epochs on which the model is executed
            epochs=200,
            # Suppress all logging
            verbose=0,
            # Compute the validation of the results on X% of the training data.
            # validation_data=
        )
        self.model.summary()

    # Collect the test results
    def test(self):
        results = self.model.evaluate(self.test_features, self.test_labels, verbose=0)

        # Evaluate the model
        #score = self.model.evaluate(self.test_features, self.test_labels, verbose=0)
        print('Test loss', results[0])
        print('Test accuracy', results[1])

        # Predict the features
        predictions = self.model.predict(self.test_features)
        print(predictions)

        results.append(sqrt(metrics.mean_squared_error(self.test_labels, predictions)))
        results.append(metrics.mean_absolute_error(self.test_labels, predictions))

        return self.results











