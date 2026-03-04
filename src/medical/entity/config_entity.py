from dataclasses import dataclass 
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_url: str 
    local_data_file: Path 
    unzip_dir: Path
    train_images_dir: Path
    train_csv_path: Path
    sample_submission_path: Path
    remove_zip_after_extraction: bool
    remove_sample_submission: bool

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    validation_status_file: Path
    required_columns: list