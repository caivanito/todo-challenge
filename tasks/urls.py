from django.urls import re_path

from tasks.views import (
    TasksList, 
    TasksAdd, 
    TasksDelete, 
    TasksComplete, 
    TasksFilters)

urlpatterns = [
    re_path(r'^tasks/list/$', TasksList.as_view()),
    re_path(r'^tasks/add/$', TasksAdd.as_view()),
    re_path(r'^tasks/delete/$', TasksDelete.as_view()),
    re_path(r'^tasks/complete/$', TasksComplete.as_view()),
    re_path(r'^tasks/filters/$', TasksFilters.as_view()),
]