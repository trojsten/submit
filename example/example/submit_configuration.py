from django.utils import timezone

from django.conf import settings
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from submit.models import Submit
from submit.views import PostSubmitForm

from submit.defaults import submit_receiver_type


class PostSubmitFormCustomized(PostSubmitForm):
    def is_submit_accepted(self, submit):
        """
        Submits after the contest has finished are automatically set to `not accepted`.
        Submit.is_accepted can be modified manually however.
        """
        task = submit.receiver.task_set.first()

        if task is None:
            return Submit.NOT_ACCEPTED

        if task.deadline < timezone.now():
            return Submit.NOT_ACCEPTED
        else:
            return Submit.ACCEPTED

    def get_success_message(self, submit):
        message = super(PostSubmitFormCustomized, self).get_success_message(submit)
        if submit.is_accepted == Submit.ACCEPTED:
            return message
        else:
            return format_html(
                u'{message}<br />{comment}',
                message=message,
                comment=_("Contest has already finished, this submit won't affect the results.")
            )


def can_post_submit(receiver, user):
    task = receiver.task_set.first()
    if task is None:
        return False
    return task.visible or user.is_staff


def display_submit_receiver_name(receiver):
    type = submit_receiver_type(receiver)

    task = receiver.task_set.first()
    if task is None:
        return 'no-task {} ({})'.format(receiver.id, type)
    return '{} ({})'.format(task.slug, type)


def display_score(review):
    task = review.submit.receiver.task_set.prefetch_related('submit_receivers').first()
    if task is None:
        return 0
    return "{:.2f}".format(review.score / (100 * len(task.submit_receivers.all())) * task.max_points)


def default_inputs_folder_at_judge(receiver):
    task = receiver.task_set.first()
    if task is None:
        return '{}-{}'.format(settings.JUDGE_INTERFACE_IDENTITY, receiver.id)
    return task.slug
