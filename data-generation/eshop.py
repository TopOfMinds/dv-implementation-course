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
        yield customer

def ingestion_time(effective_ts, mean_delay_s=60*60):
    "Ingestion time is based on a Poisson process with a mean 1 hour after effective time"
    return effective_ts + timedelta(seconds=random.expovariate(1) * mean_delay_s)

def generate_custmer_updates(customers, start, end, updates_per_day):
    customer_ids = [c["customer_id"] for c in customers]
    customer_dict = {c["customer_id"]: c for c in customers}
    # Make sure that we have an initial update for all customers at time=start
    initial_ts_customers = zip([start] * len(customer_ids), customer_ids)

    # generate updates for the customers
    ts = list(time_series(start=start, end=end, updates_per_day=updates_per_day))
    random_customer_ids = fake.random_elements(elements=customer_ids, length=len(ts))
    update_ts_customers = zip(ts, random_customer_ids)

    all_ts_customers = list(initial_ts_customers) + list(update_ts_customers)
    for t, c in all_ts_customers:
        update = {
            "date": t.isoformat(),
            "ingestion_time": ingestion_time(t).isoformat(),
            "country": "SE",
            "city": fake.city(),
            "address": fake.address()
        }
        res = customer_dict[c].copy()
        res.update(update)
        yield res

if __name__ == "__main__":
    customer_n = 10
    customers = list(generate_customers(customer_n))

    start = datetime.now() - timedelta(days=3)
    end = datetime.now() - timedelta(days=1)
    updates_per_day = 4

    customer_updates = generate_custmer_updates(customers, start, end, updates_per_day)
    for cu in customer_updates:
        print(json.dumps(cu))