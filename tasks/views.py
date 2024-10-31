import logging
logger = logging.getLogger('app')

from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework import status as status_rest
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task
from tasks.serializers import (
    TasksSerializer, 
    AddTaskSerializerValidator, 
    DeleteTaskSerializerValidator, 
    CompleteTaskSerializerValidator,
    FiltersTasksSerializerValidator
    )

from tasks.helper import get_tasks_by_filters

# Create your views here.

class TasksList(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self, request):
        try:
            user = request.user
            logger.info(f'Tareas consultadas por el usuario {user.username}')
            tasks = Task.objects.all()
            if tasks.count() > 0:
                tasks_serializer = TasksSerializer(tasks, many=True)
                return Response(data=tasks_serializer.data, status=status_rest.HTTP_200_OK)
            else:
                response = {
                        'message': "Sin tareas cargadas"
                    }
                return Response(data=response, status = status_rest.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e))
            response = {'error':str(e)}
            return Response(data=response, status=status_rest.HTTP_500_INTERNAL_SERVER_ERROR)

class TasksAdd(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request):
        try:
            user = request.user
            data = request.data
            add_task_serializer_validator = AddTaskSerializerValidator(data=data)
            if add_task_serializer_validator.is_valid():
                task = Task.objects.create(
                    title = data['title'],
                    description = data['description'],
                    user = user,
                )
                result = f'Tarea ID {task.id} creada por el usuario {user.username}'
                logger.info(result)
                
                response = {
                    'message': result
                }
                return Response(data=response, status=status_rest.HTTP_201_CREATED)
            else:
                return Response(data=add_task_serializer_validator.errors, status=status_rest.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(str(e))
            response = {'error':str(e)}
            return Response(data=response, status=status_rest.HTTP_500_INTERNAL_SERVER_ERROR)

class TasksDelete(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request):
        try:
            user = request.user
            data = request.data
            task_id = data['id']
            delete_task_serializer_validator = DeleteTaskSerializerValidator(data=data, context=user)
            if delete_task_serializer_validator.is_valid():
                task = Task.objects.get(id=task_id)
                task.delete()
                result = f'Tarea ID {task_id} borrada por el usuario {user.username}'
                logger.info(result)
                
                response = {
                    'message': result
                }
                return Response(data=response, status=status_rest.HTTP_201_CREATED)
            else:
                return Response(data=delete_task_serializer_validator.errors, status=status_rest.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(str(e))
            response = {'error':str(e)}
            return Response(data=response, status=status_rest.HTTP_500_INTERNAL_SERVER_ERROR)

class TasksComplete(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request):
        try:
            user = request.user
            data = request.data
            print(data)
            complete_task_serializer_validator = CompleteTaskSerializerValidator(data=data, context=user)
            if complete_task_serializer_validator.is_valid():
                validated_tasks = complete_task_serializer_validator.validated_data['tasks']
                tasks = Task.objects.filter(id__in=validated_tasks)
                for task in tasks:
                    task.completed = True
                    task.save()
                #tasks.update(completed=True) # no cambia la fecha de modificación, se debe iterar sobre cada objeto del queyset

                result = f'Las Tareas con ID {validated_tasks} fueron completadas por el usuario {user.username}'
                logger.info(result)
                
                response = {
                    'message': result
                }
                return Response(data=response, status=status_rest.HTTP_201_CREATED)
            else:
                return Response(data=complete_task_serializer_validator.errors, status=status_rest.HTTP_400_BAD_REQUEST)


        except Exception as e:
            logger.error(str(e))
            response = {'error':str(e)}
            return Response(data=response, status=status_rest.HTTP_500_INTERNAL_SERVER_ERROR)

class TasksFilters(APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def get(self, request):
        try:
            user = request.user
            data = request.data
            filters_tasks_serializer_validator = FiltersTasksSerializerValidator(data=data, context=user)

            if filters_tasks_serializer_validator.is_valid():
                tasks_filtered = get_tasks_by_filters(filters=data, user=user)
                if tasks_filtered is not None:
                    tasks_serializer = TasksSerializer(tasks_filtered, many=True)
                    
                    result = f'Se consultaron un total de {tasks_filtered.count()} por el usuario {user.username}'
                    logger.info(result)
                    
                    response = {
                        'message': result
                    }
                    return Response(data=tasks_serializer.data, status=status_rest.HTTP_200_OK)
                else:
                    response = {'error':'Error consultando los registros.'}
                    return Response(data=response, status=status_rest.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                return Response(data=filters_tasks_serializer_validator.errors, status=status_rest.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(str(e))
            response = {'error':str(e)}
            return Response(data=response, status=status_rest.HTTP_500_INTERNAL_SERVER_ERROR)