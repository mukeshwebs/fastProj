import random

def process_dummy_payment(user_id: int, session_id: int):
    """
    Simulates a payment process for booking a session.
    Returns True (Success) 80% of the time.
    """
    return random.random() < 0.8  # 80% success rate