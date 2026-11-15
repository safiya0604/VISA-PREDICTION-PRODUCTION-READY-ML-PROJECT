import sys
from typing import Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score
from neuro_mf import ModelFactory

from Visa_prediction.exception import Visa_predictionException
from Visa_prediction.logger import logging
from Visa_prediction.utils.main_utils import load_numpy_array_data,read_yaml_file,load_object,save_object
from Visa_prediction.entity.config_entity import ModelTrainerConfig
from Visa_prediction.entity.artifacts_entity import MODELTRAINERARTIFACT,DATATRANSFORMATIONARTIFACT,ClassificationMetricArtifact
from Visa_prediction.entity.estimator import VisaModel

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DATATRANSFORMATIONARTIFACT,
                 model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact=data_transformation_artifact
        self.model_trainer_config=model_trainer_config
#this function uses neuro_mf to get the best model object and report of the best model
    def got_model_object_and_report(self,train:np.array,test:np.array) ->Tuple[object,object]:
        try:
            logging.info("Using neuro_mf to get best model object and report")
            model_factory=ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)
            x_train,y_train,x_test,y_test=train[:,:-1],train[:,-1],test[:,:-1],test[:,-1]

            best_model_detail=model_factory.get_best_model(
                X=x_train,y=y_train,base_accuracy=self.model_trainer_config.expected_accuracy
            ) #finding the best model
            model_obj=best_model_detail.best_model #storing the best model
            y_pred=model_obj.predict(x_test) #using the best model to test data
            accuracy=accuracy_score(y_test,y_pred)
            f1=f1_score(y_test,y_pred,pos_label="Denied")
            precision=precision_score(y_test,y_pred,pos_label="Denied")
            recall=recall_score(y_test,y_pred,pos_label="Denied")
            metric_artifact=ClassificationMetricArtifact(f1_score=f1,precision_scor=precision,recall_score=recall) #saving matrix in artifact

            return best_model_detail,metric_artifact

        except Exception as e:
            raise Visa_predictionException(e,sys) from e

    def initiate_model_trainer(self,) -> MODELTRAINERARTIFACT:
        logging.info("Entered initiate_model_trainer method of model trainer class")
        #this method initiate a model trainer step

        try:
            train_arr=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)

            best_model_detail,metric_artifact=self.got_model_object_and_report(train=train_arr,test=test_arr)
            preprocessing_obj=load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                logging.info("No best model found with score more then base score")
                raise Exception("No best model found with score more than base score")

            visa_model=VisaModel(preprocessing_object=preprocessing_obj,
                                trained_model_object=best_model_detail.best_model)
            logging.info("Created visa model object with preprocessor and model")
            logging.info("Created best model file path")
            save_object(self.model_trainer_config.trained_model_file_path,visa_model)

            model_trainer_artifact=MODELTRAINERARTIFACT(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact
            )
            logging.info(f"Model trainer artifact:{model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise Visa_predictionException(e,sys) from e