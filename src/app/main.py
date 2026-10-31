import pandas as pd
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="MLOps Lab 2 Model API")

model = joblib.load("models/model.joblib")

class ModelInput(BaseModel):
    support_calls: float
    tenure_months: float
    internet_service: str  # أو float حسب نوع البيانات الأصلي
    contract: str          # أو float حسب نوع البيانات الأصلي
    monthly_charges: float

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict(data: ModelInput):
    input_df = pd.DataFrame([{
        "support_calls": data.support_calls,
        "tenure_months": data.tenure_months,
        "internet_service": data.internet_service,
        "contract": data.contract,
        "monthly_charges": data.monthly_charges
    }])
    
    prediction = model.predict(input_df)
    return {"prediction": prediction.tolist()}