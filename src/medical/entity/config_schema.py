from pydantic import BaseModel
from pathlib import Path

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

class ConfigSchema(BaseModel):
    artifacts_root: Path
    data_ingestion: DataIngestionSchema