from pathlib import Path
import json
import pickle
import mlflow
import mlflow.sklearn
import pandas as pd
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from breastCancer.utils.common import save_json
from breastCancer.entity.config_entity import ModelEvaluationConfig


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def log_into_mlflow(self):
        with open(self.config.model_path, 'rb') as f:
            model = pickle.load(f)

        with open(self.config.scaler_path, 'rb') as f:
            scaler = pickle.load(f)

        data = pd.read_csv(self.config.data_path)
        X = data.drop([self.config.target_column], axis=1)
        y = data[self.config.target_column]

        X = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        mlflow.set_registry_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            y_pred = model.predict(X_test)

            metrics_report = classification_report(
                y_test, y_pred, output_dict=True)
            save_json(path=Path(self.config.metric_path), data=metrics_report)

            mlflow.log_params(self.config.all_params)

            with open(Path(self.config.metric_path)) as f:
                metrics_report = json.load(f)
                for key, value in metrics_report.items():
                    if isinstance(value, dict):
                        for metric_name, metric_value in value.items():
                            metric_key = f"{key}_{metric_name}"
                            mlflow.log_metric(metric_key, metric_value)
                    else:
                        mlflow.log_metric(key, value)

            if tracking_url_type_store != 'file':
                mlflow.sklearn.log_model(
                    model, "model", registered_model_name="LogisticRegressionModel", serialization_format="cloudpickle")
            else:
                mlflow.sklearn.log_model(
                    model, "model", serialization_format="cloudpickle")
