from faker import Faker
import random

fake = Faker()

def brand_payload(**overrides):
    name = f"{fake.last_name()} {random.choice(['Tools', 'Hardware', 'Equipment', 'Pro'])}"
    slug = name.lower().replace(' ', '-')
    payload = {
        "name": name,
        "slug": slug
    }
    payload.update(overrides)
    return payload