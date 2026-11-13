import pymongo
import certifi #it help with connection timeout issues
import os

from Visa_prediction.exception import Visa_predictionException
from Visa_prediction.logger import logging
from Visa_prediction.constants import DATABASE_NAME,MONGODB_URL_KEY


ca=certifi.where()

class MongoDBClient:
 client=None

def __init__(self,database_name=DATABASE_NAME) -> None:
    try:
        if MongoDBClient.client is None:
            mongo_db_url=os.getenv(MONGODB_URL_KEY)
            if mongo_db_url is None:
                raise Exception(f"Enviroment key:{MONGODB_URL_KEY} is not set")
            MongoDBClient.client=pymongo.MangoClient(mango_db_url,tlsCAFile=ca)
        self.client=MongoDBClient.client
        self.database=self.client[database_name]
        self.database_name=database_name
        logging.info("MongoDB connection successful")
    except Exception as e:
        raise Visa_predictionException(e,sys)

#this is done is config folder to minize the mess as if sometime we need to make connection with db we just call this class and connection will be made so instead ofwriting the whole code in 1 file we create different different file.
