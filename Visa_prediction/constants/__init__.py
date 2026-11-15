import os
from datetime import datetime


DATABASE_NAME="VISA_PREDICTION"
COLLECTION_NAME="visa_data"
CONNECTION_URL="mongodb+srv://safiyaansari1215_db_user:<qvQD88aA3BMg4dgl>@cluster0.ridzqry.mongodb.net/?compressors=zlib"
MONGODB_URL_KEY="MONGODB_URL" #ENVIRONMENT VARIABLE

PIPELINE_NAME:str="visaprediction"
ARTIFACT_DIR:str="artifact"

FILE_NAME:str="visaprediction.csv"

TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"

TARGET_COLUMN="case_status"
CURRENT_YEAR=datetime.today().year
PREPROCESSING_OBJECT_FILE_NAME="preprocessing.pkl"
SCHEMA_FILE_PATH=os.path.join("config","schema.yaml")



file_path="notebook/data.csv"
DATA_DIR="notebook"
DATA_FILE_NAME="data.csv"
MODEL_FILE_NAME="model.pkl"

DATA_INGESTION_COLLECTION_NAME:str="visa_data"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2


DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str="report.yaml"


DATA_TRANSFORMATION_DIR_NAME:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str="transformed_object"


MODEL_TRAINER_DIR_NAME:str="model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str="trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str="model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float=0.6 #req when w push model in production
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH:str=os.path.join("config","model.yaml")


AWS_ACCESS_KEY_ID_ENV_KEY="AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV_KEY="AWS_SECRET_ACCESS_KEY_ID"
REGION_NAME="ap-southeast-2"


MODEL_EVAL_CHANGED_THRESHOLD_SCORE:float=0.02 #INCREASED
MODEL_BUCKET_NAME="visa-prediction-model2026"
MODEL_PUSHER_S3_KEY="model_registry"

APP_HOST="0.0.0.0"
APP_PORT=8080