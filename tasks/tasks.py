import logging
logger = logging.getLogger('app')

from datetime import datetime, timezone

from invera_tasks.celery import app

from tasks.models import Task

@app.task
def update_tasks():
    try:
        tasks = Task.objects.filter(completed = False)
        for task in tasks:
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            created_date = task.date_created.replace(tzinfo=None)
            diference = now - created_date
            diference_minutes = diference.seconds / 60 # si pasó mas de una que se creó la tarea cambiar el estado a completada
            if diference_minutes >= 60:
                print("SE CAMBIA ESTADO")
                task.completed = True
                task.save()
                print(task.id)

    except Exception as e:
        logger.error(str(e))