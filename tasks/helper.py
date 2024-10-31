import logging
logger = logging.getLogger('app')

from django.contrib.auth.models import User
from datetime import datetime, timedelta

from tasks.models import Task

def get_tasks_by_filters(filters:dict, user:User):
    try:
        if 'date_from' in filters:
            date_from = filters['date_from']
            if 'date_to' in filters:
                date_to = filters['date_to']
            else:
                date_to = datetime.today()
        else:
            date_from = datetime.today() - timedelta(hours=24)
            date_to = datetime.today()

        if 'contains_title' in filters:
            contains_title = filters['contains_title']
        else:
            contains_title = None
        
        if contains_title is not None:
            tasks = Task.objects.filter(
                date_created__range=(date_from, date_to),
                title__icontains=contains_title,
                user=user
            )
        else:
            tasks = Task.objects.filter(
                date_created__range=(date_from, date_to),
                user = user
            )
        print(tasks)
        return tasks.order_by('id')

    except Exception as e:
        logger.error(str(e))
        return None
