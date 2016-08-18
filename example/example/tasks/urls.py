from django.conf.urls import url

from example.tasks.views import task_list, task_statement

urlpatterns = [
    url(r'^$', task_list, name='task_list'),
    url(r'^(?P<task_slug>[\w-]+)/$', task_statement, name='task_statement'),
]
