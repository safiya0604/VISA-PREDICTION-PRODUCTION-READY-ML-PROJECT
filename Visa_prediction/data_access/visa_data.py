import sys
from typing import Optional
import numpy as np
import pandas as pd

from Visa_prediction.configuration.mongodb_connection import MongoDBClient
from Visa_prediction.constants import DATABASE_NAME
from Visa_prediction.exception import Visa_predictionException
"""This class will help to export entire mongodb record as padas dataframe"""
# class Visa_Prediction:
#     def __init__(self):
#         try:
#             self.mongo_client=MongoDBClient(database_name=DATABASE_NAME)
#         except Exception as e:
#             raise Visa_predictionException (e,sys)

#     def export_collection_as_dataframe(self,connection_name:str,database_name:Optional[str]) -> pd.DataFrame:
#         try:
#             if database_name is None:
#                 collection=self.mongo_client.database[collection_name]
#             else:
#                 collection=self.mongo_client[database_name][collection_name]

#             df=pd.DataFrame(list(collection.find()))
#             if "_id" in df.columns.to_list():
#                 df=df.drop("_id",axis=1)
#             df.replace({"na":np.nan},inplace=True)
#             return df
#         except Exception as e:
#             raise Visa_predictionException(e,sys)
                            
            
class Visa_Prediction:
    def __init__(self):
        pass
    def read_csv(self,file_path):
        try:
            df=pd.read_csv(file_path)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise Visa_predictionException(e,sys)
