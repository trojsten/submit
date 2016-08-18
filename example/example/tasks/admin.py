from django.contrib import admin

from example.tasks.models import Task


class ReceiverInline(admin.TabularInline):
    model = Task.submit_receivers.through
    extra = 0
    readonly_fields = ('get_receiver_configuration',)

    def get_receiver_configuration(self, obj):
        return obj.submitreceiver.configuration
    get_receiver_configuration.short_description = 'configuration'


class TaskAdmin(admin.ModelAdmin):
    exclude = ('submit_receivers', )
    list_display = ('slug', 'name', 'deadline', 'max_points', 'visible')
    search_fields = ('name', 'slug')
    inlines = [
        ReceiverInline,
    ]

admin.site.register(Task, TaskAdmin)
