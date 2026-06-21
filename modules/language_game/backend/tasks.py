import os
from celery import Celery

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', '6379')

celery_app = Celery(
    'language_game_tasks',
    broker=f'redis://{redis_host}:{redis_port}/0',
    backend=f'redis://{redis_host}:{redis_port}/0'
)

@celery_app.task
def generate_pdf_report_async(employee_id):
    """
    Simulates asynchronous PDF report compilation for employees.
    In a real app, this generates a nice PDF and uploads it or mails it.
    """
    print(f"Celery: Generating PDF report for employee {employee_id}...")
    import time
    time.sleep(5)
    print(f"Celery: PDF report generated successfully for employee {employee_id}.")
    return {"status": "completed", "employee_id": employee_id}
