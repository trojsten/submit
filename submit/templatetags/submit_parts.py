from django import template

from submit.constants import ReviewResponse
from submit.forms import submit_form_factory
from submit.models import Submit

register = template.Library()


@register.inclusion_tag('submit/parts/submit_form.html')
def submit_form(receiver, redirect, user, caption=None):
    """
    Renders submit form (or link) for specified SubmitReceiver.
    If the receiver doesn't have form (or link), nothing will be rendered.
    """
    data = {
        'user_can_post_submit': receiver.can_post_submit(user),
        'receiver': receiver,
        'redirect_to': redirect,
    }

    if receiver.has_form:
        data['submit_form'] = submit_form_factory(receiver=receiver)
        data['caption'] = receiver.caption or caption

    return data


@register.inclusion_tag('submit/parts/submit_list.html')
def submit_list(receiver, user):
    """
    List of all submits for specified user and receiver.
    """
    submits = Submit.with_reviews.filter(receiver=receiver, user=user).order_by('-time', '-pk')

    data = {
        'user_has_admin_privileges': receiver.has_admin_privileges(user),
        'receiver': receiver,
        'submits': submits,
        'response': ReviewResponse,
        'Submit': Submit,
    }
    return data


@register.filter
def verbose(obj, msg):
    """
    Use to print verbose versions of `constants.JudgeTestResult` or `constants.ReviewResponse`.
    """
    return obj.verbose(msg)
