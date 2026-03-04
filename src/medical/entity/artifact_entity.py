from dataclasses import dataclass 
from pathlib import Path 
from typing import Optional

@dataclass(frozen=True)
class DataIngestionArtifact:
    unzip_dir: Path
    train_images_dir: Path 
    train_csv_path: Path

@dataclass(frozen=True)
class DataValidationArtifact:
    validation_status: bool 
    validated_train_csv_path: Path
    validated_train_images_dir: Path
    