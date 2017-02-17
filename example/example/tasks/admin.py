from django.contrib import admin

from example.tasks.models import Task
from submit.admin import SubmitReceiverFromTemplateInline


class TaskAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'deadline', 'max_points', 'visible')
    search_fields = ('name', 'slug')
    inlines = [
        SubmitReceiverFromTemplateInline,
    ]

admin.site.register(Task, TaskAdmin)
