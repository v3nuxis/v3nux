from datetime import datetime, timedelta
import queue
import threading
import time
import random

OrderRequestBody = tuple[str, datetime]


storage = {
    "users": [],
    "dishes": [
        {
            "id": 1, 
            "name": "Salad",
            "value": 1099,
            "restaurant": "Silpo",
        },
        {
            "id": 2, 
            "name": "Soda",
            "value": 199,
            "restaurant": "Silpo",
        },
        {
            "id": 3,
            "name": "Pizza",
            "value": 599,
            "restaurant": "Kvadrat",
        },
    ],
    # ...
}


class Scheduler:
    def __init__(self):
        self.orders: queue.Queue[OrderRequestBody] = queue.Queue()
        self.delivery_queue: queue.Queue[OrderRequestBody] = queue.Queue()

    def process_orders(self) -> None:
        print("SCHEDULER PROCESSING...")

        while True:
            order = self.orders.get(True)

            time_to_wait = order[1] - datetime.now()

            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)
                time.sleep(0.5)
            else:
                print(f"\n\t{order[0]} SENT TO SHIPPING DEPARTMENT")
                self.delivery_queue.put(order)

    def add_order(self, order: OrderRequestBody) -> None:
        self.orders.put(order)
        print(f"\n\t{order[0]} ADDED FOR PROCESSING")

class DeliveryHandler:
    def __init__(self, delivery_queue: queue.Queue):
        self.delivery_queue = delivery_queue
        self.providers = {"uklon": 0, "uber": 0}

    def process_delivery(self) -> None:
        print("DELIVERY HANDLER STARTED...")
        while True:
            order = self.delivery_queue.get(True)
            provider = min(self.providers, key=self.providers.get)
            self.providers[provider] += 1
            print(f"\n\tProcessing delivery for order {order[0]} with provider: {provider}")

            if provider == "uklon":
                time.sleep(3)
                print(f"\n\tOrder {order[0]} delivered by Uklon!")
            elif provider == "uber":
                time.sleep(3)
                print(f"\n\tOrder {order[0]} delivered by Uber!")

            self.providers[provider] -= 1



"""""""""
Как должно работать!!
    # user input:
    # A 5 (in 5 days)
    # B 3 (in 3 days)
    После нужно подождать 3 секунды, и будет написано каким провайдером будет произведен заказ.
    
"""""""""
def main():
    scheduler = Scheduler()
    delivery_handler = DeliveryHandler(scheduler.delivery_queue)
    scheduler_thread = threading.Thread(target=scheduler.process_orders, daemon=True)
    delivery_thread = threading.Thread(target=delivery_handler.process_delivery, daemon=True)

    scheduler_thread.start()
    delivery_thread.start()


    while True:
        order_details = input("Enter order details: ")
        data = order_details.split(" ")
        order_name = data[0]
        delay = datetime.now() + timedelta(seconds=int(data[1]))
        scheduler.add_order(order=(order_name, delay))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        raise SystemExit(0)

"""""""""
Дмитрий, у меня вопрос возник при работе с кодом😅😅😅😅.Можно ли этот пайтон код в сайт запустить или перенести данные в html код при этом чтобы не требовалось переписывать?
Или если попросить ии?

"""""""""