# Generate fake e-shop data
# python3 -m pip install Faker
import json
import random
from datetime import datetime, timedelta
from faker import Faker
fake = Faker('sv_SE')

def time_series(
    start = datetime.now() - timedelta(days=10),
    end = datetime.now() - timedelta(days=1),
    updates_per_day = 4
):
    dt = start
    while dt < end:
        yield dt
        delta_seconds = random.expovariate(updates_per_day) * 24 * 60 * 60
        dt += timedelta(seconds=delta_seconds)
    

def generate_customers(n, start_id=0):
    for i in range(n):
        first_name = fake.first_name()
        last_name = fake.last_name()
        customer = {
            "customer_id": start_id + i,
            "date": fake.date_time().isoformat(),
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name}.{last_name}@{fake.domain_name()}",
            "preferred_payment_type": fake.credit_card_provider(),
            "occupation": fake.job(),
            "cell_number": fake.phone_number(),
        }
        print(json.dumps(customer))

if __name__ == "__main__":
    generate_customers(3)

    ts = time_series()
    for i in ts:
        print(i)
