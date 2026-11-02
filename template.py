import os
from pathlib import Path

project_name="Visa_prediction"

list_of_files=[
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluationm.py",
    f"{project_name}/components/model_pusher.py",
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/entity/artifacts_entity.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/pipeline/prediction_pipeline.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py"
]


for filepath in list_of_files:
    path=Path(filepath)
    filedir,filename=os.path.split(path)
    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
    if (not os.path.exists(path)) or (os.path.getsize(path)==0):
        with open(path,"w") as f:
            pass
    else:
        print(f"File is already present at :{path}")