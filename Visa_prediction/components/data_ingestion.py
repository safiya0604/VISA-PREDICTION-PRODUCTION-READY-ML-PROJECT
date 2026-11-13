import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from Visa_prediction.exception import Visa_predictionException
from Visa_prediction.logger import logging
from Visa_prediction.data_access.visa_data import Visa_Prediction
from Visa_prediction.entity.config_entity import DataIngestionConfig
from Visa_prediction.entity.artifacts_entity import DATAINGESTIONARTIFACT

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        try:
            self.data_ingestion_config=data_ingestion_config

        except Exception as e:
            raise Visa_predictionException(e,sys) from e

    def export_data_into_feature_store(self)->DataFrame:
        try:
            logging.info(f"Exporting data from mongodb")
            visa_prediction=Visa_Prediction()
            # dataframe=Visa_prediction.export_collection_as_dataframe(
            # collection_name=self.data_ingestion_config.collection_name
            dataframe=visa_prediction.read_csv(
                file_path=self.data_ingestion_config.file__path
            )
            logging.info(f"Shape of dataframe{dataframe.shape}")
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Saving exported data into feature store file path:{feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe

        except Exception as e:
            raise Visa_predictionException(e,sys)

    def split_data_as_train_test(self,dataframe:DataFrame)->None:
        logging.info(f"Entered split_data_as_train_test method of Data_ingestion class")
        try:
            train_set,test_set=train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info(f"Performed train test split on the dataframe")
            logging.info(f"Exited split_data_as_train_test method of Data_ingestion class")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            # dira_path=os.path.dirname(self.data_ingestion_config.testing_file_path)
            # os.makedirs(dira_path,exist_ok=True)

            logging.info(f"Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info(f"Exported train and test file path")
        except Exception as e:
            raise Visa_predictionException(e,sys) from e
            

    def initiate_data_ingestion(self)-> DATAINGESTIONARTIFACT:
        logging.info(f"Entered initiate_data_ingestion method of Data_ingestion class")

        try:
            dataframe=self.export_data_into_feature_store()
            logging.info("Got the data from mongodb")
            self.split_data_as_train_test(dataframe)
            logging.info("Performed train test split on the dataset")
            logging.info("Exited the initiate_data_ingestion method of Data_Ingestion class")

            data_ingestion_artifact=DATAINGESTIONARTIFACT(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path)
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise Visa_predictionException(e,sys) from e