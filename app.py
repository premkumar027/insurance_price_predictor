from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle 
import pandas as pd
import numpy as np

# import the model
pickle_model_path = 'model.pkl'
with open(pickle_model_path, 'rb') as f:
    model = pickle.load(f)


app = FastAPI()

# pydantic model to validate the input data
class InsuranceData(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=125, description='Age of the user')]
    sex: Literal['male', 'female'] = Field(..., description='Gender of the user')
    weight: Annotated[float, Field(..., gt=0, lt=250, description='Weight of the user')]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description='Height of the user')]
    children: Annotated[int, Field(..., ge=0, lt=5, description='Number of children user has')]
    smoker: Literal['yes', 'no'] = Field(..., description='Does user smoke?')
    region: Literal['northwest', 'southwest', 'northeast', 'southeast'] = Field(..., description="Where does user live?")

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def age_squared(self) -> int:
        return self.age**2
    
    @computed_field
    @property
    def smoker_age(self) -> int:
        return self.age * (1 if self.smoker == 'yes' else 0)
    
    @computed_field
    @property
    def smoker_bmi(self) -> float:
        return self.bmi * (1 if self.smoker == 'yes' else 0)


@app.post('/predict')
def predict_insurance_price(data: InsuranceData):

    input_df =pd.DataFrame([{
        'age': data.age,
        'sex': data.sex,
        'bmi': data.bmi,
        'children': data.children,
        'smoker': data.smoker,
        'region': data.region,
        'age_squared': data.age_squared,
        'smoker_age': data.smoker_age,
        'smoker_bmi': data.smoker_bmi
    }])

    prediction = model.predict(input_df)[0]
    actual_prediction = float(np.expm1(prediction))

    return JSONResponse(status_code=200, content={'predicted amount': round(actual_prediction, 2)})

