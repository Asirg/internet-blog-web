from core.celery import app


@app.task
def celery_task():
    print("!!!!!!!!!")
    return "task done!!!"

@app.task
def celery_beat_task():
    for i in range(1, 10):
        return f"task{i} done!!!"