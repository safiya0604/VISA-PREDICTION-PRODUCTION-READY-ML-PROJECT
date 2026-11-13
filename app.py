from fastapi import FastAPI,Request #rquest is used to access info sent by the client  to the app/srver
from fastapi.middleware.cors import CORSMiddleware #it helps configure which origins can access your backend
from fastapi.responses import Response #ALLOW YOU SEND RESPONSE BACK TO CLEINT
from fastapi.staticfiles import StaticFiles #SERVE STATIC FILE
from fastapi.templating import Jinja2Templates #RENDER HTML PAGES
from starlette.responses import HTMLResponse,RedirectResponse #SENDS HTML RESPONSE ND redirect the client to another url
from uvicorn import run as app_run

from typing import Optional

from Visa_prediction.constants import APP_HOST,APP_PORT
from Visa_prediction.pipeline.prediction_pipeline import VisaData,VisaClassifier 
from Visa_prediction.pipeline.training_pipeline import TrainPipeline

#creates fastapi application

app=FastAPI()

#connect static folder to fast api :urlprefix,telling api where the file is located,giving name to mounted application
app.mount("/static",StaticFiles(directory="static"),name="static")

#connect html template with fastapi
templates=Jinja2Templates(directory="templates")

#defining all (*) origins can access the backend through cors
origins=["*"]

#middleware is code that operates around http request nd response it check first then it reach endpoint/browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
class DataForm:
    def __init__ (self,request:Request):#request is http request frm the browser
        self.request:Request=request #stores the incoming request inside the object as it will be accessed by developer as imfo submited by the user  later;it is saying we are storing this particular req as object bc we will need it later bc it contain form data
        # this object allow other methods of the class to acess that request
        self.continent:Optional[str]=None
        self.education_of_employee:Optional[str]=None
        self.has_job_experience:Optional[str]=None
        self.requires_job_training:Optional[str]=None
        self.no_of_employees:Optional[str]=None
        self.company_age:Optional[str]=None
        self.region_of_employment:Optional[str]=None
        self.prevailing_wage:Optional[str]=None
        self.unit_of_wage:Optional[str]=None
        self.full_time_position:Optional[str]=None
       
    async def get_visa_data(self):
        form=await self.request.form() #.form() exctracts tje submitted form self.req is http req of browser await waits for the async operations to complete
        #since the data that is fetched from req and store in form variable is in the form of dict
        #now we are getting each feature data using dic(form) function .get that return value(value by user) for key(feature)
        self.continent=form.get("continent") #self.feature name has changed from none to user value           
        self.education_of_employee=form.get("education_of_employee")
        self.has_job_experience=form.get("has_job_experience")
        self.requires_job_training=form.get("requires_job_training")
        self.no_of_employees=form.get("no_of_employees")
        self.company_age=form.get("company_age")
        self.region_of_employment=form.get("region_of_employment")
        self.prevailing_wage=form.get("prevailing_wage")
        self.unit_of_wage=form.get("unit_of_wage")
        self.full_time_position=form.get("full_time_position")

@app.get("/",tags=["authentication"])
async def index(request:Request):
    return templates.TemplateResponse(
        "index.html",{"request":request,"context":"Rendering"}
    )
import os

print("Current directory:", os.getcwd())
print("Static folder exists:", os.path.exists("static"))
print("CSS file exists:", os.path.exists("static/style.css"))
@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline=TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training Successfull")

    except Exception as e:
        raise Response(f"Error occurred:{e}")

@app.post("/")
async def predictRouteClient(request:Request):
    try:
        form=DataForm(request)
        await form.get_visa_data()
        
        visa_data=VisaData(
            continent=form.continent,
            education_of_employee=form.education_of_employee,
            has_job_experience=form.has_job_experience,
            requires_job_training=form.requires_job_training,
            no_of_employees=form.no_of_employees,
            company_age=form.company_age,
            region_of_employment=form.region_of_employment,
            prevailing_wage=form.prevailing_wage,
            unit_of_wage=form.unit_of_wage,
            full_time_position=form.full_time_position
        )

        visa_df=visa_data.get_visa_input_data_frame() 
        model_predictor=VisaClassifier()
        value=model_predictor.predict(dataframe=visa_df)[0]

        status=None
        if value==1:
            status="Visa-approved"
        else:
            status="Visa-Not Approved"
        return templates.TemplateResponse(
            "index.html",
            {"request":request,"context":status}
        )
    except Exception as e:
        return {"status":False,"error":f"{e}"}

if __name__=="__main__":
    app_run(app,host=APP_HOST,port=APP_PORT)