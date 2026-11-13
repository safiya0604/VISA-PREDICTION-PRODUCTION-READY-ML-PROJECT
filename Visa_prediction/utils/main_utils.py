import os
import sys

import numpy as np
import dill #it is used to read python object
import yaml
from pandas import DataFrame

from Visa_prediction.exception import Visa_predictionException
from Visa_prediction.logger import logging

def read_yaml_file(file_path:str) ->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise Visa_predictionException(e,sys) from e

def write_yaml_file(file_path:str,content:object,replace:bool=False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True) #it extract dir name from file path(os.path.dirname) nd then creates a dir(os.makedirs) and save model in it with the help of w function
        with open(file_path ,"w") as file:
            yaml.dump(content,file)

    except Exception as e:
        raise Visa_predictionException (e,sys) from e



def load_object(file_path:str) -> object:
    logging.info("Entered the load_object method of utils")
    try:
        with open(file_path,"rb") as file_obj:
            obj=dill.load(file_obj)

        logging.info("Exited the load_object method of utils")
        return obj
    except Exception as e:
        raise Visa_predictionException(e,sys) from e

def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array) #this function save "array" in file(.npy file)
    except Exception as e:
        raise Visa_predictionException(e,sys) from e

def load_numpy_array_data(file_path:str) -> np.array:
    try:
        with open(file_path,"rb") as obj_file:
            return np.load(obj_file,allow_pickle=True)
    except Exception as e:
        raise Visa_predictionException(e,sys) from e


def save_object(file_path:str,obj:object) ->None:
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
        logging.info("Exited the save object method of utils")
    except Exception as e:
        raise Visa_predictionException(e,sys) from e

def drop_columns(df:DataFrame,cols:list) -> DataFrame:
    try:
        df=df.drop(columns=cols,axis=1)

        logging.info("Exited the drop_columns method of utils")

        return df
    except Exception as e:
        raise Visa_predictionException(e,sys) from e