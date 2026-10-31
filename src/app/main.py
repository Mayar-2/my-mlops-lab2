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
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="MLOps Lab 2 Model API")

# تحميل الموديل المحفوظ مسبقاً
model = joblib.load("models/model.pkl")  # أو المسار الصحيح لملف الموديل لديكِ

# تعريف Pydantic Schema للبيانات القادمة
class ModelInput(BaseModel):
    feature1: float
    feature2: float
    # أضيفي باقي الخصائص (Features) بحسب موديلك

@app.post("/predict")
def predict(data: ModelInput):
    # تجهيز البيانات وإجراء التوقع
    input_data = [[data.feature1, data.feature2]]
    prediction = model.predict(input_data)
    return {"prediction": prediction.tolist()}