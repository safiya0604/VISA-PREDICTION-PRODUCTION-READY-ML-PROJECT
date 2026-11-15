import boto3
import os
from Visa_prediction.constants import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_SECRET_ACCESS_KEY_ENV_KEY,REGION_NAME

class s3Client:
    s3_client=None
    s3_resource=None

    def __init__(self,region_name=REGION_NAME):
        #this class gets aws credentials from env_variable and creates a connection with s3 bucket and raise exception when environment is not set
        if s3Client.s3_client==None or s3Client.s3_resource==None:

            __access_key_id=os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY,)
            __secret_access_key=os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY,)

            __access_key_id=AWS_ACCESS_KEY_ID_ENV_KEY
            __secret_access_key=AWS_SECRET_ACCESS_KEY_ENV_KEY
            if __access_key_id is None:
                raise Exception(f"Environment variable :{AWS_ACCESS_KEY_ID_ENV_KEY} is not found")
            if __secret_access_key is None:
                raise Exception(f"Environment variable:{AWS_SECRET_ACCESS_KEY_ENV_KEY} is not found")

            s3Client.s3_resource=boto3.resource("s3",
                                                aws_access_key_id=__access_key_id,
                                                aws_secret_access_key=__secret_access_key)
            s3Client.s3_client=boto3.client("s3",
                                                aws_access_key_id=__access_key_id,
                                                aws_secret_access_key=__secret_access_key,
                                           region_name=region_name
                                           )
            self.s3_resource=s3Client.s3_resource
            self.s3_client=s3Client.s3_client