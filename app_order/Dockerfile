FROM python:3.10

WORKDIR /app_order

# Установка зависимостей проекта
COPY ./requirements.txt /app_order/
RUN pip install --no-cache-dir --upgrade -r /app_order/requirements.txt

# Перенос проекта в образx
COPY ./app /app_order/app
COPY .env /app_order

# Копирование файлов alembic
COPY ./migration /app_order/migration
COPY ./alembic.ini /app_order/alembic.ini

EXPOSE 8084

# Добавляем путь к корневому каталогу проекта в PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app_order"
ENV PYTHONPATH="${PYTHONPATH}:/app_order/app"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8084"]