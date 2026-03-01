from dataclasses import dataclass 
from pathlib import Path 
from typing import Optional

@dataclass(frozen=True)
class DataIngestionArtifact:
    zip_file_path: Path
    extracted_dir: Path
    dataset_dir: Path 
    train_dir: Path
    metadata_file_path: Optional[Path]
    download_status: bool