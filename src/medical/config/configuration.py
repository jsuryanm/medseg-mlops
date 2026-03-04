import os 
from pathlib import Path

from src.medical.constants import *
from src.medical.utils.common import read_yaml,create_directories
from src.medical.entity.config_schema import ConfigSchema
from src.medical.entity.config_entity import (DataIngestionConfig,
                                              DataValidationConfig)

class ConfigurationManager:
    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath=PARAMS_FILE_PATH):
        
        self.config = read_yaml(config_filepath,ConfigSchema)
        self.params = read_yaml(params_filepath)
        
        # artifacts_root can be accessed as a dict
        create_directories([self.config.artifacts_root])

    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(root_dir=config.root_dir,
                                                    source_url=config.source_url,
                                                    local_data_file=config.local_data_file,
                                                    unzip_dir=config.unzip_dir,
                                                    train_images_dir=config.train_images_dir,
                                                    train_csv_path=config.train_csv_path,
                                                    sample_submission_path=config.sample_submission_path,
                                                    remove_zip_after_extraction=config.remove_zip_after_extraction,
                                                    remove_sample_submission=config.remove_sample_submission)
        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(root_dir=config.root_dir,
                                                      validation_status_file=config.validation_status_file,
                                                      required_columns=config.required_columns)
        return data_validation_config