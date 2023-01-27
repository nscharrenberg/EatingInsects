from tensorflow import keras

from app.networks.shared.BaseNetwork import BaseNetwork


class LR(BaseNetwork):
    def compile(self):
        if self.model:
            raise Exception("Model has already been compiled")

        self.model = keras.Sequential([
            keras.layers.Dense(1)
        ])

        self.model.compile(
            loss=keras.metrics.mean_absolute_error,
            optimizer=keras.optimizers.Adam(float(self.predictor.learning_rate)),
            metrics=[
                keras.metrics.RootMeanSquaredError(name="RMSE")
            ]
        )

        return self.model
