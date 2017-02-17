from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

import submit.settings as submit_settings
from submit.models import Submit


def is_submit_accepted(submit):
    """
    This method defines which submits will be accepted, penalized or not accepted.
    This method is called after the submit is created, but before it is saved in database.
    e.g. submits after deadline are not accepted
    """
    return Submit.ACCEPTED


def form_success_message(submit):
    """
    Returned message will be added to `messages` after successful submit via form.
    """
    if submit.receiver.send_to_judge:
        return format_html(
                _('Submit successful. Testing protocol will be soon available <a href="{link}">here</a>.'),
                link=reverse('view_submit', args=[submit.id])
        )
    return _('Submit successful.')


def prefetch_data_for_score_calculation(reviews_qs):
    return reviews_qs


def display_score(review):
    return str(review.score)


def render_review_comment(review):
    return review.comment


def submit_receiver_type(receiver):
    if '.zip' in receiver.get_extensions() and receiver.send_to_judge:
        return 'testable zip'
    if receiver.send_to_judge:
        return 'source'
    if receiver.has_form:
        return 'description'
    if receiver.external_link or receiver.allow_external_submits:
        return 'external'
    return 'other'


def display_submit_receiver_name(receiver):
    return '{} ({})'.format(receiver.id, submit_receiver_type(receiver))


def default_inputs_folder_at_judge(receiver):
    return '{}-{}'.format(submit_settings.JUDGE_INTERFACE_IDENTITY, receiver.id)


def can_post_submit(receiver, user):
    return True


def has_admin_privileges_for_receiver(receiver, user):
    return user.is_staff
