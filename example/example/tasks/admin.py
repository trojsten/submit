from django.contrib import admin

from example.tasks.models import Task

from submit.models import SubmitReceiver


class ReceiverInline(admin.StackedInline):
    model = SubmitReceiver
    extra = 0
    show_change_link = True
    readonly_fields = ('configuration', )


class TaskAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'deadline', 'max_points', 'visible')
    search_fields = ('name', 'slug')
    inlines = [
        ReceiverInline,
    ]

admin.site.register(Task, TaskAdmin)
