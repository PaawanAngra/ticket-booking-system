from locust import HttpUser, task, between

class TicketUser(HttpUser):
    wait_time = between(1, 2)

    @task(1)
    def view_event(self):
        self.client.get("/events/1")

    @task(3)
    def attempt_booking(self):
        payload = {
            "event_id": 2,
            "user_id": 1
        }
        self.client.post("/book", json=payload, name="/book")