# When the submit app gets its own repository, these definitions will be moved to testovac/submit/

from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from testovac.submit.defaults import submit_receiver_type
from testovac.submit.models import Submit
from testovac.submit.views import PostSubmitForm


class PostSubmitFormCustomized(PostSubmitForm):
    def can_post_submit(self, receiver, user):
        if not receiver.task_set.all():
            return False
        task = receiver.task_set.all()[0]
        return task.is_visible_for_user(user)

    def is_submit_accepted(self, submit):
        if not submit.receiver.task_set.all():
            return Submit.NOT_ACCEPTED
        task = submit.receiver.task_set.all()[0]

        if task.contest.has_finished():
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


def display_submit_receiver_name(receiver):
    type = submit_receiver_type(receiver)

    if not receiver.task_set.all():
        return False
    task_slug = receiver.task_set.all()[0].slug

    return '{} ({})'.format(task_slug, type)




