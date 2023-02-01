from core.celery import app
import time 


@app.task
def test_task(arg):
    time.sleep(2)
    print("!"*100)
    return arg