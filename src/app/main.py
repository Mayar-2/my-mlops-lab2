from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# تعريف نموذج البيانات باستخدام Pydantic للتحقق من المدخلات
class ModelInput(BaseModel):
    feature1: float
    feature2: float

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict")
def predict(data: ModelInput):
    # سيتم تمرير البيانات للنموذج هنا
    result = data.feature1 * 0.5 + data.feature2 * 0.5
    return {"prediction": result}