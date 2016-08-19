from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from example.tasks.models import Task


def task_list(request):
    tasks = Task.objects.all()
    if not request.user.is_staff:
        tasks = tasks.filter(visible=True)

    return render(
        request,
        'tasks/task_list.html',
        {'tasks': tasks},
    )


def task_statement(request, task_slug):
    task = get_object_or_404(Task, pk=task_slug)
    if not task.visible and not request.user.is_staff:
        raise PermissionDenied()

    return render(
        request,
        'tasks/task_statement.html',
        {'task': task},
    )
