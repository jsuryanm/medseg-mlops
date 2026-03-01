from src.medical.config.configuration import ConfigurationManager
from src.medical.components.data_ingestion import DataIngestion
from src.medical.logger import logger 
from src.medical.exceptions import MedException
import sys

STAGE_NAME = "Data Ingestion stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<\nx=======x")
    except Exception as e:
        logger.exception(e)
        raise MedException(e,sys)    
