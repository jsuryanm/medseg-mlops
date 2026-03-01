import os
import yaml
from pydantic import BaseModel
from src.medical.logger import logger
from src.medical.exceptions import MedException
import json
from pathlib import Path
import sys 

import random 
import numpy as np 
import torch 

def read_yaml(path_to_yaml: Path, schema: BaseModel):
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
        
        logger.info(f"yaml file:{path_to_yaml} loaded successfully")
        return schema.model_validate(content) 
        # validates data from dict or another class instance to create new model instance
    except Exception as e:
        logger.error(f"Error loading JSON:{path_to_yaml}")
        raise MedException(e,sys)
    
def create_directories(paths: list[Path],verbose: bool = True):
    try:
        for path in paths:
            os.makedirs(path,exist_ok=True)
            if verbose:
                logger.info(f"created directory at: {path}")
        
    except Exception as e:
        logger.error("Directory creation failed")
        raise MedException(e,sys)
    
def save_json(path: Path, data: dict):
    try:
        with open(path,"w") as f:
            json.dump(data,f,indent=4)
        
        logger.info(f"json file saved at: {path}")
    
    except Exception as e:
        raise MedException(e,sys)

def load_json(path: Path,schema: BaseModel):
    try:
        with open(path) as f:
            content = json.load(f)
            
        logger.info(f"json file loaded successfully from: {path}")
        return schema.model_validate(content)
    except Exception as e:
        raise MedException(e,sys)

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    