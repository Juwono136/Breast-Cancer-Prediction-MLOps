import pandas as pd
from breastCancer import logger
from breastCancer.entity.config_entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def get_clean_data(self):
        data = pd.read_csv(self.config.data_path)
        data = data.drop(['Unnamed: 32', 'id'], axis=1)

        data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})

        data.to_csv(self.config.data_clean_path, index=False)

        logger.info("Data has been cleaned.")

        return data
