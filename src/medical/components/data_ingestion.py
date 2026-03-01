import os 
import zipfile 
import gdown 
import shutil
from pathlib import Path 
import sys

from src.medical.entity.config_entity import DataIngestionConfig
from src.medical.entity.artifact_entity import DataIngestionArtifact
from src.medical.utils.common import set_seed

from src.medical.logger import logger 
from src.medical.exceptions import MedException

import random 

class DataIngestion:
    def __init__(self,config: DataIngestionConfig):
        self.config = config
        set_seed()

    def download_file(self) -> str:
        """Fetches data from url"""
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
            
        except Exception as e:
            raise MedException(e,sys)