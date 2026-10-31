import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="MLOps Lab 2 Model API")

# تحميل الموديل المحفوظ مسبقاً
model = joblib.load("models/model.joblib")

# تعريف Pydantic Schema للبيانات القادمة (تأكدي من مطابقتها لخصائص موديلك)
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
    # تجهيز البيانات وإجراء التوقع باستخدام الموديل الحقيقي
    input_data = [[data.feature1, data.feature2, data.feature3, data.feature4, data.feature5]]
    prediction = model.predict(input_data)
    return {"prediction": prediction.tolist()}