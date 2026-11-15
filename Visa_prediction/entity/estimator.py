import sys

from pandas import DataFrame
from sklearn.pipeline import Pipeline

from Visa_prediction.exception import Visa_predictionException
from Visa_prediction.logger import logging

class TargetValueMapping:
    def __init__(self):
        self.Certified:int=0
        self.Denied:int=1

    def _asdict(self):
        return
        self.__dict__

    def reverse_mapping(self):
        mapping_response=self._asdict()
        return dict(zip(mapping_response.values(),mapping_response.keys()))


class VisaModel:
    def __init__(self,preprocessing_object:Pipeline,trained_model_object:object):
        self.preprocessing_object=preprocessing_object #INPUT OBJECT OF PREPROCESSOR
        self.trained_model_object=trained_model_object #INPUT OBJECT OF TRAINED MODEL

#THIS FUNCTION ACCEPTS RAW INPUTS AND THEN TRANSFORMED RAW INPUT USING PREPROCESSING_OBJECT WHICH GARUNTEE THAT HTE INPUT ARE IN THE SAME FORMAT AS THE TRAINING DATA AT LAST IT PERFORMS PREDICTION ON TRANSFORMED FEATURES
    def  predict(self,dataframe:DataFrame) ->DataFrame:
        logging.info("Entered predict method of UTruckModel class")
        try:
            logging.info("using the trained model to get predictions")
            transformed_feature=self.preprocessing_object.transform(dataframe)
            logging.info("using the trained model to get prediction")
            return self.trained_model_object.predict(transformed_feature)
        except Exception as e:
            raise Visa_predictionException(e,sys) from e


    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"