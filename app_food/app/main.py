import asyncio

from fastapi import FastAPI

from microservice_food_app.app_food.app import rabbitmq
from microservice_food_app.app_food.app.endpoints.food_router import food_router


app = FastAPI(title='Service')


loki_logs_handler = LokiHandler(
    url="http://loki:3100/loki/api/v1/push",
    tags={"application": "fastapi"},
    version="1",
)
logger = logging.getLogger("uvicorn.access")
logger.addHandler(loki_logs_handler)


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))


app.include_router(food_router, prefix='/api')
