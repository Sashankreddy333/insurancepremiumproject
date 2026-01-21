from fastapi import FastAPI,Path,HTTPException, Query
from pydantic import BaseModel,Field,computed_field
from typing import Literal, Annotated, Optional
import json
import pickle
import pandas as pd
from pydantic.responses import JSONResponse

app=FastAPI()
with open("model.pkl","rb")as f:
    model=pickle.load(f)
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]
class patient(BaseModel):
    age:Annotated[int,Field(..., description="age of the patient",gt=0,lt=100)]
    weight:Annotated[float,Field(...,description="patient weight",gt=0)]
    height:Annotated[float,Field(...,description="patient height in m",gt=0)]
    income_lpa:Annotated[float,Field(...,description="income",gt=0)]
    smoker:Annotated[bool,Field(...,description="is Smoker")]
    city:Annotated[str,Field(...,description="city")]
    occupation:Annotated[str,Field(...,description="occupation of the patient")]
    
    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/(self.height**2),2)
    @computed_field
    @property
    def agegroup(self)->str:
        if self.age<25:
            return "young"
        elif self.age<45:
            return "adult"
        elif self.age<60:
            return "middleage"
        return "senior"
    @computed_field
    @property
    def lifestylerisk(self)->str:
        if self.smoker and self.bmi>30:
            return "high"
        elif self.smoker and self.bmi>27:
               return "medium"
        else:
            return "low"
    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
    