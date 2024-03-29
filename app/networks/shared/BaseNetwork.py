from django.core.files.storage import default_storage
from tensorflow import keras

from app.business import predictors
from app.models import Predictor, Protein
from app.networks.utils.processing_utils import ProcessingUtils

import tensorflow as tf


class BaseNetwork:
    def __init__(self, predictor: Predictor):
        tf.random.set_seed(int(predictor.seed))
        tf.keras.utils.set_random_seed(int(predictor.seed))
        tf.config.experimental.enable_op_determinism()

        self.results = None
        self.location = 'resources/public/networks/{}.h5'.format(predictor.slug)
        self.predictor = predictor
        self.compiled = False
        self.model = None
        X, y = ProcessingUtils.load_dataset(predictor.dataset, predictors.get_prediction_type_by_key(predictor.prediction_type))
        self.dataset_train, self.dataset_test = ProcessingUtils.load_train_and_test_sets(X, y, predictor)
        self.train_labels = None
        self.test_features = None
        self.train_features = None
        self.test_labels = None

        self.extract_features()

        if self.predictor.location and default_storage.exists(self.predictor.location):
            self.model = keras.models.load_model(self.predictor.location)
        else:
            self.compile()
            self.train()

    def extract_features(self):
        if self.dataset_train is None or self.dataset_test is None:
            raise Exception("Unable to extract features, as the train or test set are not loaded.")

        self.train_features = self.dataset_train.copy()
        self.test_features = self.dataset_test.copy()
        self.train_labels = self.train_features.pop(predictors.get_prediction_type_by_key(self.predictor.prediction_type))
        self.test_labels = self.test_features.pop(predictors.get_prediction_type_by_key(self.predictor.prediction_type))

    def compile(self):
        raise Exception("Model has not yet been implemented.")

    def train(self):
        self.model.fit(
            self.train_features,
            self.train_labels,
            validation_split=float(self.predictor.split),
            verbose=0,
            epochs=int(self.predictor.epochs),
        )

        self.model.save(self.location)
        self.predictor.location = self.location
        self.predictor.save()

    def test(self):
        self.results = self.model.evaluate(self.test_features, self.test_labels, verbose=0)

        return self.results

    def predict(self, protein: Protein):
        model_input = protein.to_dataFrame()
        return self.model.predict(model_input)
