from django.core.files.storage import default_storage
from tensorflow import keras

from app.models import Predictor, Protein
from app.networks.utils.processing_utils import ProcessingUtils


class BaseNetwork:
    def __init__(self, predictor: Predictor):
        self.results = None
        self.location = 'resources/public/networks/{}.h5'.format(predictor.slug)
        self.predictor = predictor
        self.compiled = False
        self.model = None
        X, y = ProcessingUtils.load_dataset(predictor.dataset)
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
        self.train_labels = self.train_features.pop('Solubility(%)')
        self.test_labels = self.test_features.pop('Solubility(%)')

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
