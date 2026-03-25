from datetime import datetime

def safe_round(value, digits=2):
    try:
        return round(float(value), digits)
    except Exception:
        return None

def now_text():
    return datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")