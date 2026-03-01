import yaml 
import json 
from pathlib import Path 
from typing import Dict
from pydantic import validate_call
from src.medical.exceptions import MedException
from src.medical.logger import logger
import sys

@validate_call
def read_yaml(path: Path) -> Dict:
    """
    Read YAML file safely
    """
    try:
        if not path.exists():
            raise FileNotFoundError(f"YAML file not found: {path}")
        
        with open(path) as f:
            data = yaml.safe_load(f)

        if data is None:
            raise ValueError("YAML file is empty")
        
        logger.info(f"YAML loaded from {path}")
        return data
    
    except Exception as e:
        logger.error(f"Error reading YAML: {path}")
        raise MedException(e,sys)
    
@validate_call
def create_directories(paths: list[Path],verbose: bool = True):
    try:
        for path in paths:
            path.mkdir(parents=True,exist_ok=True)
            if verbose:
                logger.info(f"Created directory: {path}")
    except Exception as e:
        logger.error("Directory creation failed")
        raise MedException(e,sys)

@validate_call
def save_json(path: Path, data: Dict):
    try:
        path.parent.mkdir(parents=True,exist_ok=True)

        with open(path,"w") as f:
            json.dump(data,f,indent=4)

        logger.info(f"JSON saved at {path}")

    except Exception as e:
        logger.error(f"Error saving JSON:{path}")
        raise MedException(e,sys)
    
@validate_call
def load_json(path: Path) -> Dict:
    try:
        if not path.exists():
            raise FileNotFoundError(path)

        with open(path) as f:
            data = json.load(f)

        logger.info(f"JSON loaded from {path}")
        return data

    except Exception as e:
        logger.error(f"Error loading JSON: {path}")
        raise MedException(e)
