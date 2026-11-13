from dataclasses import dataclass

@dataclass
class DATAINGESTIONARTIFACT:
    trained_file_path:str
    test_file_path:str


@dataclass
class DATAVALIDATIONARTIFACT:
    validation_status:bool
    message:str
    drift_report_file_path:str

@dataclass
class DATATRANSFORMATIONARTIFACT:
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str



@dataclass
class ClassificationMetricArtifact:
    f1_score:float
    precision_scor:float
    recall_score:float


@dataclass
class MODELTRAINERARTIFACT:
    trained_model_file_path:str
    metric_artifact:ClassificationMetricArtifact


@dataclass
class MODELEVALUAITONARTIFACT:
    is_model_accepted:bool
    changed_accuracy:float
    s3_model_path:str
    trained_model_path:str

@dataclass
class MODELPUSHERARTIFACT:
    bucket_name:str
    s3_model_path:str
    