import sys

from Visa_prediction.exception import Visa_predictionException
from Visa_prediction.logger import logging
from Visa_prediction.entity.config_entity import ModelPusherConfig
from Visa_prediction.entity.artifacts_entity import MODELPUSHERARTIFACT,MODELEVALUAITONARTIFACT
from Visa_prediction.entity.s3_estimator import VisaEstimator
from Visa_prediction.cloud_storage.aws_storage import SimpleStorageService


class ModelPusher:
    def __init__(self,model_evaluation_artifact:MODELEVALUAITONARTIFACT,
                model_pusher_config:ModelPusherConfig):
        self.model_eval_artifact=model_evaluation_artifact
        self.model_pusher_config=model_pusher_config
        self.s3=SimpleStorageService
        self.visa_estimator=VisaEstimator(bucket_name=ModelPusherConfig.bucket_name,
                                         model_path=model_pusher_config.s3_model_key_path)

    def initiate_model_pusher(self) -> MODELPUSHERARTIFACT:
        logging.info("Entered inititate_model_pusher method of model trainer class")
        try:
            logging.info("Uploading artifacts folder to s3 bucket")
            self.visa_estimator.save_model(from_file=self.model_eval_artifact.trained_model_path)

            model_pusher_artifact=MODELPUSHERARTIFACT(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.s3_model_key_path)

            logging.info("Uploading artifacts folder to s3 bucket")
            logging.info(f"Model pusher artifact:[{model_pusher_artifact}]")
            logging.info("Exited the initiate_model_pusher method of Modeltrainer class")

            return model_pusher_artifact
        except Exception as e:
            raise Visa_predictionException(e,sys) from e