from src.medical.config.configuration import ConfigurationManager
from src.medical.components.data_validation import DataValidation
from src.medical.entity.artifact_entity import DataValidationArtifact 
from src.medical.logger import logger 
from src.medical.exceptions import MedException
import sys

STAGE_NAME = "Data Validation stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self,data_ingestion_artifact):
        config = ConfigurationManager()
        
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config,
                                         data_ingestion_artifact=data_ingestion_artifact)
        
        data_validation_artifact = data_validation.initiate_data_validation()
        return data_validation_artifact