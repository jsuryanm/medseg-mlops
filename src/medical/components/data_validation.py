import sys 
import pandas as pd 
from PIL import Image
from pathlib import Path
import json

from src.medical.entity.config_entity import DataValidationConfig
from src.medical.entity.artifact_entity import (DataIngestionArtifact,
                                                DataValidationArtifact)
from src.medical.exceptions import MedException
from src.medical.logger import logger 
from src.medical.utils.common import save_json

class DataValidation:
    def __init__(self,
                 config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        
        self.config = config
        self.data_ingestion_artifact = data_ingestion_artifact
    
    def validate_csv_schema(self,df:pd.DataFrame) -> bool:
        """Validate the csv schema"""
        required_columns = self.config.required_columns
        
        logger.info("Validating the csv file")
        
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Missing required column:{col}")
                return False
        
        logger.info("CSV schema validation passed")
        return True
    
    def validate_images(self,image_dir: Path) -> bool:
        logger.info("Validating images")
        # rglob finds recursively all files and driectories matching a specific pattern
        for img_path in image_dir.rglob("*.png"):
            try:
                with Image.open(img_path) as img:
                    img.verify()
                    # checks if file broken without fully decoding img 
            except Exception:
                logger.error(f"Corrupt image detected:{img_path}")
                return False
        
        logger.info("Image validation passed")
        return True
    
    def validate_rle_masks(self, df: pd.DataFrame) -> bool:

        logger.info("Validating RLE masks")

        for rle in df["segmentation"].dropna():

            tokens = rle.split()

            if len(tokens) % 2 != 0:
                logger.error(f"Invalid RLE detected: {rle}")
                return False

        logger.info("RLE validation passed")
        return True
    
    def is_data_validated(self) -> bool:
        """Check if the data validation completed"""

        if self.config.validation_status_file.exists():

            try:
                with open(self.config.validation_status_file) as f:
                    status = json.load(f)
                
                if status.get("validation_status") is True:
                    logger.info("Data validation is already completed. Skipping the data validation component.")
                    return True
                
            except Exception:
                logger.warning("Validation status file exists but could not be read.")
        
        return False


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            if self.is_data_validated():
                logger.info("Skipping data validation")
                return DataValidationArtifact(validation_status=True,
                                                              validated_train_csv_path=train_csv_path,
                                                              validated_train_images_dir=train_images_dir)


            train_csv_path = self.data_ingestion_artifact.train_csv_path
            train_images_dir  = self.data_ingestion_artifact.train_images_dir
            
            logger.info("Creating a pandas dataframe after reading train.csv")
            df = pd.read_csv(train_csv_path)
            
            schema_status = self.validate_csv_schema(df)
            image_status = self.validate_images(train_images_dir)
            rle_status = self.validate_rle_masks(df)

            validation_status = schema_status and rle_status and image_status
            logger.info(f"Validation status: {validation_status}")

            save_json(path=self.config.validation_status_file,
                      data={"validation_status":validation_status})
            
            data_validation_artifact = DataValidationArtifact(validation_status=validation_status,
                                                              validated_train_csv_path=train_csv_path,
                                                              validated_train_images_dir=train_images_dir)
            return data_validation_artifact
        
        except Exception as e:
            raise MedException(e,sys)