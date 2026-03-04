from pydantic import BaseModel
from pathlib import Path
from typing import List

class DataIngestionSchema(BaseModel):
    root_dir: Path
    source_url: str
    local_data_file: Path
    unzip_dir: Path
    train_images_dir: Path
    train_csv_path: Path
    sample_submission_path: Path
    remove_zip_after_extraction: bool
    remove_sample_submission: bool

class DataValidationSchema(BaseModel):
    root_dir: Path
    validation_status_file: Path
    required_columns: List[str]

class ConfigSchema(BaseModel):
    artifacts_root: Path
    data_ingestion: DataIngestionSchema
    data_validation: DataValidationSchema
