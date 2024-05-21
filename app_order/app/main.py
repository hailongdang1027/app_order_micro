import asyncio
import logging

from fastapi import FastAPI
# from logging_loki import LokiHandler
from microservice_food_app.app_order.app import rabbitmq
from microservice_food_app.app_order.app.endpoints.order_router import order_router

app = FastAPI(title='Service')


# loki_logs_handler = LokiHandler(
#     url="http://loki:3100/loki/api/v1/push",
#     tags={"application": "fastapi"},
#     version="1",
# )
# logger = logging.getLogger("uvicorn.access")
# logger.addHandler(loki_logs_handler)


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume(loop))


app.include_router(order_router, prefix='/api')
