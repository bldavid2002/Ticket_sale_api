import asyncio
import json
import aio_pika
import asyncpg

DB_URL = "postgresql://postgres:password@postgres:5432/ticketing"
AMQP_URL = "amqp://guest:guest@rabbitmq:5672/"


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = json.loads(message.body.decode())
        print(f"Received message for user {body['user_id']}: {body}")
        conn = await asyncpg.connect(DB_URL)
        await conn.execute('''
            INSERT INTO reservations (user_id, item_id, quantity, section, row, seat_number, timestamp, price_cents)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        ''', body['user_id'], body['item_id'], body['quantity'], body['section'], body['row'], body['seat_number'], body['timestamp'], body['price_cents'])
        await conn.close()

        print("Succesfully saved reservation to database.")

async def main():
    connection = await aio_pika.connect_robust(AMQP_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("reservation_queue", durable=True)

    print("Waiting for messages...")
    await queue.consume(process_message)

    try:
        await asyncio.Future()  
    finally:
        await connection.close()

if __name__ == "__main__":
    asyncio.run(main())