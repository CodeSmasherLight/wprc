from .redis_client import redis_client

def set_state(contact_number: str, step: str, product: str = "", name: str = ""):
    redis_client.hset(f"state:{contact_number}", mapping={
        "step": step,
        "product": product,
        "name": name
    })
    redis_client.expire(f"state:{contact_number}", 3600)  # expire in 1 hour

def get_state(contact_number: str):
    data = redis_client.hgetall(f"state:{contact_number}")
    if not data or "step" not in data:
        return None
    return data

def clear_state(contact_number: str):
    redis_client.delete(f"state:{contact_number}")
