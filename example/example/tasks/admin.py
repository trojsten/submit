from django.contrib import admin
from django.db import models
from django.forms import TextInput

from example.tasks.models import Task

from submit.models import SubmitReceiver


class ReceiverInline(admin.TabularInline):
    model = SubmitReceiver
    extra = 0
    show_change_link = True

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '15'})},
    }


class TaskAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'deadline', 'max_points', 'visible')
    search_fields = ('name', 'slug')
    inlines = [
        ReceiverInline,
    ]

admin.site.register(Task, TaskAdmin)
