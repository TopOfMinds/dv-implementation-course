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

def generate_customer_updates(customers, start, end, updates_per_day):
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
    
def generate_products(n, start_id=0):
    colors = "black|white|grey|brown|yellow|red|green|blue|beige".split("|")
    product_types = "couch|chair|armchair|carpet".split("|")
    product_names = "GRÖNLID|LANDSKRONA|SÖDERHAMN|EKTORP|KIVIK|VIMLE|ÄPPLARYD|BACKSÄLEN|PÄRUP|LÅNGARYD|KLUBBFORS|VINLIDEN|LINANÄS|VALLENTUNA|KLIPPAN|GLOSTAD|FÄRLÖV|RINGSTORP|BARKTORP|KLINTORP|SPEDTORP".split("|")
    for i in range(n):
        product = {
            "product_id": start_id + i,
            "product_type": fake.random_element(elements=product_types),
            "product_name": fake.random_element(elements=product_names),
            "color": fake.random_element(elements=colors),
            "price": fake.random_int(min=999, max=10000, step=500),
        }
        yield product

def generate_sales_lines(customers, products, start, end, sales_per_day):
    customer_ids = [c["customer_id"] for c in customers]
    product_ids = [p["product_id"] for p in products]
    product_price = {p["product_id"]: p["price"] for p in products}
    print(product_price)
    ts = time_series(start=start, end=end, updates_per_day=updates_per_day)

    for i, t in enumerate(ts):
        product_id = fake.random_element(elements=product_ids)
        quantity = fake.random_int(min=1, max=4, step=1)
        price = product_price[product_id]
        sl = {
            "sales_line_id": i,
            "date": t.isoformat(),
            "ingestion_time": ingestion_time(t).isoformat(),
            "customer_id": fake.random_element(elements=customer_ids),
            "product_id": product_id,
            "payment_type": fake.credit_card_provider(),
            "quantity": quantity,
            "price": price,
            "total": quantity * price,
        }
        yield sl


if __name__ == "__main__":
    customer_n = 10
    customers = list(generate_customers(customer_n))

    start = datetime.now() - timedelta(days=3)
    end = datetime.now() - timedelta(days=1)
    updates_per_day = 4

    customer_updates = generate_customer_updates(customers, start, end, updates_per_day)
    # for cu in customer_updates:
    #     print(json.dumps(cu))

    products = list(generate_products(10))

    # for p in products:
    #     print(p)

    sales_per_day = 10
    sales_lines = generate_sales_lines(customers, products, start, end, sales_per_day)
    for sl in sales_lines:
        print(sl)
