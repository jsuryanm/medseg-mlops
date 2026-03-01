from dataclasses import dataclass 
from pathlib import Path 
from typing import Optional

@dataclass(frozen=True)
class DataIngestionArtifact:
    unzip_dir: Path
    train_images_dir: Path 
    train_csv_path: Path
    