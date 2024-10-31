from django.contrib import admin

# Register your models here.

from tasks.models import Task

class TaskAdmin(admin.ModelAdmin):
    list_per_page = 100
    search_fields = ('id', 'title', 'description', 'user__username')
    list_filter = ('completed', 'user__username')
    list_display = [
        'id',
        'title',
        'description',
        'user',
        'completed',
        'date_created',
        'date_updated',

    ]
    autocomplete_fields = ['user']

admin.site.register(Task, TaskAdmin)