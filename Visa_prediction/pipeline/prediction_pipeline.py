import os
import sys

import numpy as np
import pandas as pd
from Visa_prediction.entity.config_entity import VisaPredictorConfig
from Visa_prediction.entity.s3_estimator import VisaEstimator
from Visa_prediction.exception import Visa_predictionException
from Visa_prediction.logger import logging

from Visa_prediction.utils.main_utils import read_yaml_file
from pandas import DataFrame


class VisaData:
    def __init__(self,
                 continent,
                 education_of_employee,
                 has_job_experience,
                 requires_job_training,
                 no_of_employees,
                 company_age,
                 region_of_employment,
                 prevailing_wage,
                 unit_of_wage,
                 full_time_position
                ):
        try:
            self.continent=continent
            self.education_of_employee=education_of_employee
            self.has_job_experience=has_job_experience
            self.requires_job_training=requires_job_training
            self.no_of_employees=no_of_employees
            self.company_age=company_age
            self.region_of_employment=region_of_employment
            self.prevailing_wage=prevailing_wage
            self.unit_of_wage=unit_of_wage
            self.full_time_position=full_time_position

        except Exception as e:
            raise Visa_predictionException(e,sys) from e

    def get_visa_input_data_frame(self) ->DataFrame:
        """This function return a dataframe from visa data input"""
        try:
            visa_input_dict=self.get_visa_data_as_dict()
            return DataFrame(visa_input_dict)
        except Exception as e:
            raise Visa_predictionException(e,sys) from e

    def get_visa_data_as_dict(self):
        """This function returns a dictionary from visa data class input"""
        logging.info("Entered get_visa_data_as dict method of visa_data class")
        try:
            input_data={
                "continent":[self.continent],
                "education_of_employee":[self.education_of_employee],
                "has_job_experience":[self.has_job_experience],
                "requires_job_training":[self.requires_job_training],
                "no_of_employees":[self.no_of_employees],
                "company_age":[self.company_age],
                "region_of_employment":[self.region_of_employment],
                "prevailing_wage":[self.prevailing_wage],
                "unit_of_wage":[self.unit_of_wage],
                "full_time_position":[self.full_time_position]
            }

            logging.info("Created visa_data dict")
            logging.info("Exited the get_visa_data_dict method of visa_data class")
            return input_data

        except Exception as e:
            raise Visa_predictionException(e,sys) from e


class VisaClassifier:
    def __init__(self,prediction_pipeline_config:VisaPredictorConfig=VisaPredictorConfig(),)->None:
        """Param prediction_pipeline_config :configuration for prediction the value"""
        try:
            self.prediction_pipeline_config=prediction_pipeline_config
        except Exception as e:
            raise Visa_predictionException(e,sys) from e

    def predict(self,dataframe) ->str:
        """This is the method od visaclassifier class that return prediction in string format"""
        try:
            logging.info("Entered predict method of VisaClassifier class")
            model=VisaEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path
            )
            result=model.predict(dataframe)
            return result

        except Exception as e:
            raise Visa_predictionException(e,sys) from e