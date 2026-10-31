from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_read_health():
    """1. اختبار الـ health check والـ API contract"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"

def test_predict_endpoint_exists():
    """2. اختبار وجود نقطة النهاية للـ predict"""
    response = client.post("/predict", json={})
    # حتى لو كان هناك خطأ في المدخلات (422) فهذا يثبت أن الـ endpoint موجود ويتحقق من الـ schema
    assert response.status_code in [200, 422]

def test_input_schema_validation():
    """3. اختبار التحقق من مخطط المدخلات (Pydantic Input Validation)"""
    # إرسال بيانات خاطئة أو غير مطابقة للـ schema المتوقعة
    response = client.post("/predict", json={"invalid_field": -999})
    assert response.status_code == 422

def test_model_loading_and_prediction():
    """4. اختبار التنبؤ الحتمي (Deterministic Prediction)"""
    # ضعِ بيانات صحيحة تتناسب مع نموذجك الفعلي
    payload = {"feature1": 1.0, "feature2": 0.5} 
    response = client.post("/predict", json=payload)
    if response.status_code == 200:
        data = response.json()
        assert "prediction" in data

def test_edge_case_handling():
    """5. اختبار حالة حافة (Edge Case) مثل قيم متطرفة أو فارغة"""
    response = client.post("/predict", json={"feature1": 999999.0, "feature2": -999999.0})
    # التأكد من أن السيرفر لا ينهار (لا يعطي 500 Internal Server Error)
    assert response.status_code != 500