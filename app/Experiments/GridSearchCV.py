# Author: Raghav RV <rvraghav93@gmail.com>
# License: BSD

import pandas as pd
from sklearn.model_selection import GridSearchCV

from sklearn.tree import DecisionTreeRegressor

from app.models.Dataset import Dataset
from app.networks.DT.DT import DT
from app.models import Predictor, ModelType, PredictionType


# reference:https://scikit-learn.org/stable/auto_examples/model_selection/plot_multi_metric_evaluation.html#sphx-glr-auto-examples-model-selection-plot-multi-metric-evaluation-py

def get_results():
    dataset = Dataset(name="experiments Dataset", location='resources/private/datasets/sibo_dataset_example.csv')
    predictor = Predictor(model_type=ModelType.DT, prediction_type=PredictionType.SOLUBILITY, dataset=dataset,
                          slug='dt')
    dt = DT(predictor)
    X = dt.train_features
    y = dt.train_labels

    gs = GridSearchCV(
        DecisionTreeRegressor(random_state=int(dt.predictor.seed)),
        # RandomForestRegressor(random_state=int(dt.predictor.seed)),
        # Testable parameters for RF
        # n_estimators, max_depth, min_samples_split,min_samples_leaf,bootstrap, oob_score
        # Testable parameters for DT
        #  max_depth, min_samples_split,min_samples_leaf
        param_grid={'max_depth': range(2, 10, 1)},
        scoring='neg_root_mean_squared_error',
        n_jobs=-1
    )
    gs.fit(X, y)
    results = gs.cv_results_
    df = pd.DataFrame(results)
    df.to_csv('DT_max_depth.csv')

    return results
