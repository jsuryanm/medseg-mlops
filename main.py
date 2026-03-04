import sys
from src.medical.logger import logger 
from src.medical.exceptions import MedException

from src.medical.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from src.medical.pipeline.stage_02_data_validation import DataValidationTrainingPipeline

# stage 1
STAGE_NAME = "Data Ingestion stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started from main.py <<<<<<")
    data_ingestion_pipeline = DataIngestionTrainingPipeline()
    data_ingestion_artifact = data_ingestion_pipeline.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise MedException(e,sys)

# stage 2
STAGE_NAME = "Data Validation stage"
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started from main.py <<<<<<")
    validation_pipeline = DataValidationTrainingPipeline()
    validation_artifact = validation_pipeline.main(data_ingestion_artifact)
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

except Exception as e:
    raise MedException(e,sys)
