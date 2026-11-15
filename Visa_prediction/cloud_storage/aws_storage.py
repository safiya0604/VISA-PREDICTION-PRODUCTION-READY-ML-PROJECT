import boto3
from Visa_prediction.configuration.aws_connection import s3Client
from io import StringIO
from typing import Union,List
import os,sys
from Visa_prediction.logger import logging
from Visa_prediction.exception import Visa_predictionException
from mypy_boto3_s3.service_resource import Bucket
from botocore.exceptions import ClientError
from pandas import DataFrame,read_csv
import pickle

class SimpleStorageService:

    def __init__(self):
        s3_client=s3Client()
        self.s3_resource=s3_client.s3_resource
        self.s3_client=s3_client.s3_client

    def s3_key_path_available(self,bucket_name,s3_key) ->bool:
        try:
            bucket=self.get_bucket(bucket_name)
            file_objects=[file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            if len(file_objects) > 0:
                return True
            else:
                return False
        except Exception as e:
            raise Visa_predictionException(e,sys)

    @staticmethod
    def read_object(object_name:str,decode:bool=True,make_readable:bool=False) -> Union[StringIO,str]:
        logging.info("Entered the read_object method of s3 operations class")
        try:
            func=(
                lambda:object_name.get()["Body"].read().decode()
                if decode is True
                else object_name.get()["Body"].read()
            )
            conv_func=lambda:StringIO(func()) if make_readable is True else func()
            logging.info("Exited the read_obj method od s3 operations class")
        except Exception as e:
            raise Visa_predictionException(e,sys)


    def get_bucket(self,bucket_name:str) ->Bucket:
        logging.info("Entered the get_Bucket method of s3 operations class")
        try:
            bucket=self.s3_resource.Bucket(bucket_name)
            logging.info("Exited the get_bucket method of s3 operations class")
            return bucket
        except Exception as e:
            raise Visa_predictionException(e,sys)


    def get_file_object(self,file_name:str,bucket_name:str) ->Union [List[object],object]:
        logging.info("Entered get_file_object method od s3 operations class")
        try:
            bucket=self.get_bucket(bucket_name)
            file_objects=[file_object for file_object in bucket.objects.filter(Prefix=file_name)]
            func=lambda x :x[0] if len(x) ==1 else x

            file_objs=func(file_objects)
            logging.info("Exited the get_file_object method of s3 operations class")

            return file_objs
        except Exception as e:
            raise Visa_predictionException(e,sys)


    def load_model(self,model_name:str,bucket_name:str,model_dir:str=None) ->object:
        logging.info("Entered the load_model method of s3 operations")
        try:
            func=(
                lambda:model_name
                if model_dir is None
                else model_dir+"/"+model_name
            )
            model_file=func()
            file_object=self.get_file_object(model_file,bucket_name)
            model_obj=self.read_object(file_object,decode=False)
            model=pickle.load(model_obj)
            logging.info("Exited the load_model method of s3 operations class")
        except Exception as e:
            raise Visa_predictionException(e,sys)

    def create_folder(self,folder_name:str,bucket_name:str) -> None:
        logging.info("Entered the create_folder method of s3 operations class")
        try:
            self.s3_client.put_object(Bucket=bucket_name,Key=folder_obj)
        except ClientError as e:
            if e.response["Errors"]["Code"]=="404":
                folder_obj=folder_name + "/"
                self.s3_client.put_object(Bucket=bucket_name,Key=folder_obj)
            else:
                pass
            logging.info("Exited the create_folder method of s3 operations class")

    def upload_file(self,from_filename:str,
                    to_filename:str,bucket_name:str,remove:bool=True):
        logging.info("Entered the upload_file method od s3 operations class")
        try:
            logging.info(f"Uploading {from_filename} file to {to_filename} file in {bucket_name} bucket.")

            self.s3_resource.meta.client.upload_file(
            from_filename,
            bucket_name,
            to_filename
        )

            logging.info("File successfully uploaded to S3")
            
            
            
            if remove is True:
                os.remove(from_filename)
                logging.info(f"Remove is set to {remove} ,deleted the file")
            else:
                logging.info(f"Remove is set to {remove} , not deleted the file")
            logging.info("Exited the upload_file method of s3 operation class")
        except Exception as e:
            raise Visa_predictionException(e,sys)      

    def upload_df_as_csv(self,data_frame:DataFrame,local_filename:str,bucket_filename:str,bucket_name:str) -> None:
        # """This method uploads the dataframe to bucket_filename csv file in bucket_name bucket"""
        try:
            data_frame.to_csv(local_filename,index=None,header=True)
            self.upload_file(local_filename,bucket_filename,bucket_name)
            logging.info("Exited the upload_df_as_csv method of s3operations class")
        except Exception as e:
            raise Visa_predictionException(e,sys) from e

    def get_df_from_object(self,object_:object) ->DataFrame:
    # """This method gets the dataframe from the object_name object"""
        try:
            content=self.read_object(object_,make_readable=True)
            df=read_csv(content,na_Values="na")
            logging.info("Exited the get_df_from_object method of s3operations class")
            return df
        except Exception as e:
            raise Visa_predictionException(e,sys) from e

    def read_csv(self,filename:str,bucket_name:str)->DataFrame:
        # """This method get the dataframe from the object_name object"""
        logging.info("Entered the read_Csv method of s3 operation class")
        try:
            csv_obj=self.get_file_object(filename,bucket_name)
            df=self.get_df_from_object(csv_obj)
            logging.info("Exited the read csv method od s3 operations class")
            return df
        except Exception as e:
            raise Visa_predictionException(e,sys) from e