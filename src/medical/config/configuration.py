import os 
from pathlib import Path

from src.medical.constants import *
from src.medical.utils.common import read_yaml,create_directories
from src.medical.entity.config_entity import (DataIngestionConfig)

class ConfigurationManager:
    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath=PARAMS_FILE_PATH):
        
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        
        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(root_dir=Path(config.root_dir),
                                                    source_url=config.source_url,
                                                    local_data_file=Path(config.local_data_file),
                                                    unzip_dir=Path(config.unzip_dir),
                                                    dataset_dir=Path(config.train_dir))