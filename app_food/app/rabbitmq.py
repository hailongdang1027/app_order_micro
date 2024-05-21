import json
import traceback
import aio_pika

from asyncio import AbstractEventLoop
# from aio_pika import connect_robust, IncomingMessage
# from aio_pika.abc import AbstractRobustConnection
from microservice_food_app.app_food.app.repositories.db_food_repo import FoodRepo
from microservice_food_app.app_food.app.services.food_service import FoodService
from microservice_food_app.app_food.app.settings import settings


async def process_new_food(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        FoodService().create_food(data['name'], data['description'], data['price'])
    except:
        traceback.print_exc()
    finally:
        await msg.ack()


async def process_get_food(msg: IncomingMessage):
    try:
        repo = FoodRepo()
        foods = repo.get_food()
        await msg.ack()
        return foods
    except:
        await msg.ack()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    new_food_queue = await channel.declare_queue('new_food_queue', durable=True)
    getting_food_queue = await channel.declare_queue('get_foods_queue', durable=True)

    await new_food_queue.consume(process_new_food)
    await getting_food_queue.consume(process_get_food)
    print('Started consuming new food messages...')
    return connection
