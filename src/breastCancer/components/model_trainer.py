import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from breastCancer.entity.config_entity import ModelTrainerConfig
from breastCancer import logger


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        data = pd.read_csv(self.config.data_path)
        X = data.drop([self.config.target_column], axis=1)
        y = data[self.config.target_column]

        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)

        model = LogisticRegression(
            penalty=self.config.penalty, tol=self.config.tol)
        model.fit(X_train, y_train)

        # save model and scaler
        with open(self.config.model_path, 'wb') as f:
            pickle.dump(model, f)
        with open(self.config.scaler_path, 'wb') as f:
            pickle.dump(scaler, f)

        logger.info("Model has been created.")
