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
    """
    Format of displayed score can depend on other models.
    Modify a default queryset of `Review.objects` by pre-fetching data
    so that the function `display_score` won't need any additional database queries.
    """
    return reviews_qs


def display_score(review):
    """
    This function is called when a score is displayed to the user - `review.display_score()`.
    Since `review.score` holds "data without context", points that will be displayed to the user are expected to be
    calculated from `review.score` e.g. score may be a percentual value for a specific type of submit and absolute
    value for other type ...
    """
    return str(review.score)


def render_review_comment(review):
    """
    Allows tweaks such as markdown rendering.
    """
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
    """
    Used in admin to allow better identification of type of receiver.
    (Type is not a property of receiver, but can be determined from receiver attributes.)
    """
    return '{} ({})'.format(receiver.id, submit_receiver_type(receiver))


def default_inputs_folder_at_judge(receiver):
    """
    When a receiver is added to a task and `receiver.send_to_judge` is checked,
    this function will be used to automatically set the name of the folder with inputs at judge server.
    When this function is called SubmitReceiver object is created but is not saved in database yet.
    """
    return '{}-{}'.format(submit_settings.JUDGE_INTERFACE_IDENTITY, receiver.id)


def can_post_submit(receiver, user):
    """
    Defines who and when can post submits.
    e.g. some tasks may be hidden
    """
    return True


def has_admin_privileges_for_receiver(receiver, user):
    """
    Defines who can view all submits of this receiver.
    e.g. an organizator of specific competition can access all submits of all users in this competition
    """
    return user.is_staff
