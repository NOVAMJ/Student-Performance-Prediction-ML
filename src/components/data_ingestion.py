import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer
@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")

# These are the inputs that I'm giving to my data ingestion component.
# And now data ingestion component knows where to save the train path test path and data path because
# of this file path  

# Why we need this:
# When you write ML pipelines, you often need to save files in specific places (like processed data, raw data, etc.).
# Instead of hardcoding these file paths everywhere in the code, we keep them in a config class.

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Inmgestion of the data iss completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys)
        
# # Why we do each step:
# # Log start: Logs help us see what's happening and debug if needed.

# # Read dataset: Load data from CSV so we can work with it in Python.

# # Make directory: We save files into artifacts/. Make sure this folder exists.

# # Save raw data: Keep a copy of the original data before we change anything.

# # Split: Create train/test datasets for ML.

# # Save train/test: Store them for next steps (like data transformation or training).

# # Return paths: Later parts of the pipeline can use these paths.

# # Why try/except with CustomException:
# # If anything fails (bad file, wrong path, etc.), the exception is caught.

# CustomException helps wrap the error with context so logs show exactly where the error happened.
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))




 