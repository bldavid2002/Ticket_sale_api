import asyncio
import time

import httpx

URL = "http://localhost:8000/reserve"

async def buy_seat(client, user_id):
    payload = {
        "user_id": f"USR-{user_id}",
        "item_id": "EVT-999",
        "quantity": 1,
        "section": "VIP",
        "row": "A",
        "seat_number": 99, 
        "timestamp": 1792070000,
        "price_cents": 15000
    }
    response = await client.post(URL, json=payload)
    return response.status_code

async def main():
    print("fireing 500 conccurent request")
    start_time = time.time()
    async with httpx.AsyncClient() as client:
        tasks = [buy_seat(client, i) for i in range(500)]
        result = await asyncio.gather(*tasks)

    duration = time.time() - start_time
    successes = result.count(202)
    conflicts = result.count(409)

    print("\nLOAD TEST RESULTS")
    print("Total Requests: 500")
    print(f"Time Taken:   {duration:.2f} seconds")
    print(f"Successes:   {successes} (Should be EXACTLY 1)")
    print(f"Blocked:     {conflicts} (Should be 499)")

if __name__ == "__main__":
    asyncio.run(main())