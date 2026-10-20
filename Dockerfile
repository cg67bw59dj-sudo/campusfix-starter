FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# 数据库放在 /app/data，方便用 Volume 持久化
ENV DATABASE_PATH=/app/data/campusfix.db

EXPOSE 5000

# 首次启动时若数据库不存在则初始化，之后直接启动（避免每次重建 demo 数据）
CMD ["sh", "-c", "test -f \"$DATABASE_PATH\" || python init_db.py; exec python app.py"]
