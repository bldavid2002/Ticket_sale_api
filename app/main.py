import json
from contextlib import asynccontextmanager

import aio_pika
import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import logging
import asyncio


class ReservationRequest(BaseModel):
    user_id: str
    item_id: str
    quantity: int
    section: str
    row: str
    seat_number: int
    timestamp: int
    price_cents: int

redis_client = None
rabbitmq_connection = None
rabbitmq_channel = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client, rabbitmq_connection, rabbitmq_channel
    redis_client =  redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
    rabbitmq_connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672/")
    rabbitmq_channel = await rabbitmq_connection.channel()
    await rabbitmq_channel.declare_queue("reservation_queue", durable=True)
    print("Connected to Redis and RabbitMQ")
    yield
    await redis_client.close()
    await rabbitmq_connection.close()

    logger = logging.getLogger(__name__)
    max_retries = 5
    retry_delay = 3

    for attempt in range(1, max_retries + 1):
        try: 
            logger.info("Connecting to RabbitMQ (Attempt {attempt}/{max_retries})")
            rabbitmq_connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672/")
            break
        except Exception as e:
            if attempt == max_retries:
                raise e
            logger.warning("RabbitMQ not ready yet, retrying in {retry_delay}s")
            await asyncio.sleep(retry_delay)
            

app = FastAPI(title="Reservation API", lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Reservation API is running"}

@app.post("/reserve", status_code=status.HTTP_202_ACCEPTED)
async def reserve_seat(reservation_request: ReservationRequest):
    seat_id = f"seat:{reservation_request.section}:{reservation_request.row}:{reservation_request.seat_number}"
    lock_acquired = await redis_client.set(seat_id, reservation_request.user_id, nx=True, ex=180)

    if not lock_acquired:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Seat is already reserved")

    message_body = json.dumps(reservation_request.dict()).encode()
    message = aio_pika.Message(body=message_body, delivery_mode=aio_pika.DeliveryMode.PERSISTENT)
    await rabbitmq_channel.default_exchange.publish(message, routing_key="reservation_queue")

    return {"status": "success", "message": "Seat reservation request accepted", "seat_id": seat_id}
