from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from submit.models import Submit
from submit.defaults import form_success_message as default_success_message


def is_submit_accepted(submit):
    """
    Submits after the contest has finished are automatically set to `not accepted`.
    Submit.is_accepted can be modified manually however.
    """
    task = submit.receiver.task

    if task.deadline < timezone.now():
        return Submit.NOT_ACCEPTED
    else:
        return Submit.ACCEPTED


def form_success_message(submit):
    message = default_success_message(submit)
    if submit.is_accepted == Submit.ACCEPTED:
        return message
    else:
        return format_html(
            u'{message}<br />{comment}',
            message=message,
            comment=_("Contest is finished, this submit won't affect the results.")
        )


def can_post_submit(receiver, user):
    task = receiver.task
    return task.visible or user.is_staff


def prefetch_data_for_score_calculation(reviews_qs):
    return reviews_qs\
        .select_related('submit__receiver__task')\
        .prefetch_related('submit__receiver__task__submitreceiver_set')


def display_score(review):
    task = review.submit.receiver.task
    return "{:.2f}".format(review.score / (100 * len(task.submitreceiver_set.all())) * task.max_points)


def default_inputs_folder_at_judge(receiver):
    return receiver.task.slug
