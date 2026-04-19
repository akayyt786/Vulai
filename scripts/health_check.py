import os
import sys
import django
from django.db import connections
from django.db.utils import OperationalError

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

def check_db():
    db_conn = connections['default']
    try:
        db_conn.cursor()
    except OperationalError:
        return False
    else:
        return True

def check_celery():
    from celery.result import AsyncResult
    from config.celery import app
    try:
        # Ping workers
        i = app.control.inspect()
        stats = i.stats()
        if not stats:
            return False
        return True
    except Exception:
        return False

def check_redis():
    import redis
    try:
        r = redis.from_url(settings.CELERY_BROKER_URL)
        r.ping()
        return True
    except Exception:
        return False

if __name__ == "__main__":
    db_ok = check_db()
    redis_ok = check_redis()
    celery_ok = check_celery()
    
    print(f"Database: {'OK' if db_ok else 'FAILED'}")
    print(f"Redis:    {'OK' if redis_ok else 'FAILED'}")
    print(f"Celery:   {'OK' if celery_ok else 'FAILED'}")
    
    if not (db_ok and redis_ok):
        print("\nCRITICAL: Core infrastructure is down.")
        sys.exit(1)
        
    if not celery_ok:
        print("\nWARNING: No Celery workers detected. Scans will remain in 'pending' status.")
        
    sys.exit(0)
