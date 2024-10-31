from rest_framework import serializers
from django.utils import timezone

from tasks.models import Task

class TasksSerializer(serializers.Serializer):
    def to_representation(self, task:Task):
        data = {
            'title' : task.title,
            'description' : task.description,
            'user': task.user.username,
            'date_crated': task.date_created,
            'date_updated': task.date_updated,
            'completed': task.completed,
        }
        return data

class AddTaskSerializerValidator(serializers.Serializer):

    title = serializers.CharField(max_length = 200)
    description = serializers.CharField(max_length = 200)

class DeleteTaskSerializerValidator(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    
    def validate_id(self, id):
        if not Task.objects.filter(id=id, user=self.context).exists():
            raise serializers.ValidationError(f'La tarea con ID {id} no existe o no tiene permisos para eliminarla.')

class CompleteTaskSerializerValidator(serializers.Serializer):
    tasks = serializers.ListField(child = serializers.CharField(max_length = 200), required = False)

    def validate_tasks(self, tasks):
        tasks_set = set(tasks) # por posibles duplicados
        print(tasks_set)
        tasks_validated = []
        for id in tasks_set:
            if Task.objects.filter(id=id, user=self.context).exists():
                tasks_validated.append(id)
        tasks_validated.reverse()
        return tasks_validated

class FiltersTasksSerializerValidator(serializers.Serializer):
    date_from = serializers.DateTimeField(required = False)
    date_to = serializers.DateTimeField(required = False)
    contains_title = serializers.CharField(required = False)

    
    def validate_date_from(self, date_from):
        if date_from > timezone.now():
            raise serializers.ValidationError(f"La fecha elegida '{str(date_from)}' no puede ser mayor a hoy.")
        return date_from


    def validate(self, data):
        print('validate')
        print(data)
        if 'date_from' in data:
            if 'date_to' in data:
                if data['date_to'] < data['date_from']:
                    date_to = str(data['date_to'])
                    raise serializers.ValidationError(f"La fecha elegida 'date_to:' '{date_to}' no puede ser mayor que 'date_from'.")
        return data