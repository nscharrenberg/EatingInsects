from tensorflow import keras

from app.networks.shared.BaseNetwork import BaseNetwork


class SNN(BaseNetwork):
    def compile(self):
        if self.model:
            raise Exception("Model has already been compiled")

        self.model = keras.Sequential([
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dense(1)
        ])

        self.model.compile(
            loss='mean_absolute_error',
            optimizer=keras.optimizers.Adam(float(self.predictor.learning_rate)),
            metrics=[
                keras.metrics.MeanSquaredError(name="MSE"),
                keras.metrics.MeanAbsoluteError(name="MAE"),
                keras.metrics.RootMeanSquaredError(name="RMSE"),
                keras.metrics.MeanSquaredLogarithmicError(name='MSLE')
            ]
        )

        return self.model
