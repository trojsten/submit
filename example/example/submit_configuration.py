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

        if not submit.receiver.task_set.all():
            return Submit.NOT_ACCEPTED
        task = submit.receiver.task_set.all()[0]

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
    possible_tasks = receiver.task_set.all()
    if not possible_tasks:
        return False
    return possible_tasks[0].visible or user.is_staff


def display_submit_receiver_name(receiver):
    type = submit_receiver_type(receiver)

    possible_tasks = receiver.task_set.all()
    if not possible_tasks:
        return 'no-task {} ({})'.format(receiver.id, type)
    return '{} ({})'.format(possible_tasks[0].slug, type)


def display_score(review):
    possible_tasks = review.submit.receiver.task_set.all().prefetch_related('submit_receivers')
    if not possible_tasks:
        return 0
    task = possible_tasks[0]

    return "{:.2f}".format(review.score / (100 * len(task.submit_receivers.all())) * task.max_points)


def default_inputs_folder_at_judge(receiver):
    if not receiver.task_set.all():
        return '{}-{}'.format(settings.JUDGE_INTERFACE_IDENTITY, receiver.id)
    task = receiver.task_set.all()[0]
    return task.slug
