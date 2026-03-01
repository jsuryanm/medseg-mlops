import os 
import zipfile 
import gdown 
import sys

from src.medical.entity.config_entity import DataIngestionConfig
from src.medical.entity.artifact_entity import DataIngestionArtifact
from src.medical.utils.common import set_seed

from src.medical.logger import logger 
from src.medical.exceptions import MedException

class DataIngestion:
    def __init__(self,config: DataIngestionConfig):
        self.config = config
        set_seed()

    def download_file(self) -> str:
        """Downloads data from google drive url"""
        try:
            dataset_url = self.config.source_url
            zip_download_dir = str(self.config.local_data_file)
            os.makedirs(self.config.root_dir,exist_ok=True)
            logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            file_id = dataset_url.split("/")[-2]
            prefix = "https://drive.google.com/uc?/export=download&id="
            gdown.download(prefix+file_id,zip_download_dir)

            logger.info(f"Downloaded data from {dataset_url} into {zip_download_dir}")

        except Exception as e:
            raise MedException(e,sys)

    def extract_zip_file(self):
        """Extract the zip file into data directory"""
        try:
            unzip_path = self.config.unzip_dir
            os.makedirs(unzip_path,exist_ok=True)

            logger.info(f"Extracting the zip file:{self.config.local_data_file}")

            with zipfile.ZipFile(self.config.local_data_file,"r") as zip_ref:
                zip_ref.extractall(unzip_path)

            logger.info("Extraction completed")

            # remove zip file once extracted
            if self.config.remove_zip_after_extraction:
                if self.config.local_data_file.exists():
                    self.config.local_data_file.unlink()
                    logger.info("Zip file removed after extraction")
        
        except Exception as e:
            raise MedException(e,sys)
    
    def verify_dataset(self) -> None:
        """Verify the dataset structure"""
        if not self.config.train_images_dir.exists():
            raise FileNotFoundError("Train images directory missing.")
        
        if not self.config.train_csv_path.exists():
            raise FileNotFoundError("train.csv missing")
        
        logger.info("Dataset verified")
        # remove the sample submission file
        if self.config.remove_sample_submission:
            if self.config.sample_submission_path.exists():
                self.config.sample_submission_path.unlink()
                logger.info("Sample submission file removed.")
    
    def is_data_already_ingested(self) -> bool:
        """Check if data ingestion artifacts exist"""
        if (self.config.train_images_dir.exists() and 
            self.config.train_csv_path.exists()):
            logger.info("Data ingestion artifacts already exists. Skipping the data ingestion component.")
            return True
        else:
            return False
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """Starts the data ingestion component"""
        try:
            if not self.is_data_already_ingested():
                self.download_file()
                self.extract_zip_file()
                self.verify_dataset()

                data_ingestion_artifact = DataIngestionArtifact(unzip_dir=self.config.unzip_dir,
                                                                train_images_dir=self.config.train_images_dir,
                                                                train_csv_path=self.config.train_csv_path)
            return data_ingestion_artifact
         
        except Exception as e:
            raise MedException(e,sys)