import os
import shutil
from breastCancer import logger
from breastCancer.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def check_file_exist(self):
        if not os.path.exists(self.config.local_data_file):
            shutil.copy(self.config.source_data, self.config.root_dir)
            logger.info("File already exists. Data Ingestion successfully.")
        else:
            logger.info(
                "File does not exist! Please create a data folder and save the data inside it.")
