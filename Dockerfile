
# Stage 1: Builder
FROM python:3.12.12-slim AS builder

WORKDIR /build

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime
FROM python:3.12.12-slim AS runtime

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# نسخ الكود مع إعطاء الصلاحيات مباشرة للمستخدم appuser
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser models/ ./models/

# إنشاء المستخدم الآمن
RUN useradd --create-home --uid 10001 appuser

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s \
  --timeout=5s \
  --start-period=15s \
  --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)" || exit 1

# استخدام المسار الكامل للـ uvicorn داخل البيئة الافتراضية للتأكد من عمله بدون أخطاء
CMD ["/opt/venv/bin/uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
COPY models/ ./models/