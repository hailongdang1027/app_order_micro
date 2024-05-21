import json
import traceback
from asyncio import AbstractEventLoop
import aio_pika
from aio_pika import connect_robust, IncomingMessage
from aio_pika.abc import AbstractRobustConnection

from microservice_food_app.app_food.app.settings import settings
from microservice_food_app.app_order.app.services.order_service import OrderService


async def process_created_order(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        OrderService().create_order(data['items'], data['order_total'])
    except:
        traceback.print_exc()
    finally:
        await msg.ack()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    order_created_queue = await channel.declare_queue('order_created_queue', durable=True)

    await order_created_queue.consume(process_created_order)

    print('Started consuming order messages...')
    return connection
