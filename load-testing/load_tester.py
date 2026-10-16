import time
import random
from locust import HttpUser, task, between

class TicketBuyer(HttpUser):
    wait_time = between(1, 3)

    @task
    def reserve_seat(self):

        event_id = f"EVT-{random.randint(1, 10)}"
        section = random.choice(["VIP", "GA", "A", "B", "C"])
        row = random.choice(["A", "B", "C", "D", "E"])
        seat = random.randint(1, 500)
        user_id = f"USR-{random.randint(10000, 99999)}"

        payload = {
            "user_id": user_id,
            "item_id": event_id,
            "quantity": 1,
            "section": section,
            "row": row,
            "seat_number": seat,
            "timestamp": int(time.time()),
            "price_cents": 15000
        }

        with self.client.post("/reserve", json=payload, catch_response=True) as response:
            if response.status_code == 202:
                response.success()
            elif response.status_code == 409:
                response.success()
            else:
                response.failure(f"Unexpected status code: {response.status_code}")