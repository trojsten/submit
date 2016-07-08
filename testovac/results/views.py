from django.http import Http404
from django.shortcuts import get_object_or_404, render

from testovac.results.table_generator import generate_result_table
from testovac.tasks.models import Contest


def contest_results(request, contest_slug):
    contest = get_object_or_404(Contest, pk=contest_slug)
    if not contest.is_visible_for_user(request.user):
        raise Http404
    tasks = contest.task_set.all()
    max_sum = sum(tasks.values_list('max_points', flat=True))
    table_data = generate_result_table(tasks)
    return render(
        request,
        'results/contest_results_table.html',
        {'contest': contest, 'tasks': tasks, 'table_data': table_data, 'max_sum': max_sum}
    )


def contest_group_results(request, group_slug):
    return Http404
