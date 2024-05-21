FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /app_food

# Установка зависимостей проекта
COPY ./requirements.txt /app_food/
RUN pip install --no-cache-dir --upgrade -r /app_food/requirements.txt

# Перенос проекта в образ
COPY ./app /app_food/app
COPY .env /app_food

# Копирование файлов alembic
COPY ./migration /app_food/migration
COPY ./alembic.ini /app_food/alembic.ini

EXPOSE 8083

CMD ["/bin/sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8083"]

