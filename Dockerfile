# Stage 1: builder
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: runtime
FROM python:3.11-slim AS runtime

RUN groupadd --system appgroup \
 && useradd --system --gid appgroup appuser

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --chown=appuser:appgroup app.py .

EXPOSE 5000
USER appuser

CMD ["python", "app.py"]
