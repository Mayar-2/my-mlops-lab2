import pandas as pd
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="MLOps Lab 2 Model API")

model = joblib.load("models/model.joblib")

class ModelInput(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float
    feature5: float

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict(data: ModelInput):
    # تحويل المدخلات إلى Pandas DataFrame بأسماء الأعمدة المطابقة للموديل
    input_df = pd.DataFrame([{
        "feature1": data.feature1,
        "feature2": data.feature2,
        "feature3": data.feature3,
        "feature4": data.feature4,
        "feature5": data.feature5
    }])
    
    prediction = model.predict(input_df)
    return {"prediction": prediction.tolist()}