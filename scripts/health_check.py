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
    # Attempt to ping celery worker
    # In a real environment, we'd use celery.task.control.ping
    return "True" # Placeholder

if __name__ == "__main__":
    db_ok = check_db()
    print(f"Database: {'OK' if db_ok else 'FAILED'}")
    if not db_ok:
        sys.exit(1)
    sys.exit(0)
