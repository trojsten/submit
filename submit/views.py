from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response as APIResponse

import submit.settings as submit_settings
from submit.constants import JudgeTestResult, ReviewResponse
from submit.forms import submit_form_factory
from submit.judge_helpers import (JudgeConnectionError,
                                  create_review_and_send_to_judge,
                                  parse_protocol)
from submit.models import Review, Submit, SubmitReceiver
from submit.serializers import ExternalSubmitSerializer
from submit.submit_helpers import (create_submit, send_file,
                                   write_chunks_to_file)


@login_required
@require_POST
def post_submit_form(request, receiver_id):
    receiver = get_object_or_404(SubmitReceiver, pk=receiver_id)

    if not receiver.can_post_submit(request.user):
        raise PermissionDenied()

    if receiver.has_form:
        form = submit_form_factory(request.POST, request.FILES, receiver=receiver)
    else:
        raise PermissionDenied()

    if form.is_valid():
        submit = create_submit(user=request.user, receiver=receiver, sfile=request.FILES['submit_file'])
    else:
        for field in form:
            for error in field.errors:
                messages.add_message(request, messages.ERROR, u"%s: %s" % (field.label, error))
        for error in form.non_field_errors():
            messages.add_message(request, messages.ERROR, error)
        return redirect(request.POST['redirect_to'])

    if receiver.send_to_judge:
        try:
            create_review_and_send_to_judge(submit)
        except JudgeConnectionError:
            messages.add_message(request, messages.ERROR, _('Upload to judge was not successful.'))
            return redirect(request.POST['redirect_to'])

    messages.add_message(request, messages.SUCCESS, import_string(submit_settings.SUBMIT_FORM_SUCCESS_MESSAGE)(submit))
    return redirect(request.POST['redirect_to'])


@login_required
def view_submit(request, submit_id):
    submit = get_object_or_404(Submit.objects.select_related('receiver', 'user'), pk=submit_id)
    user_has_admin_privileges = submit.receiver.has_admin_privileges(request.user)

    if submit.user != request.user and not user_has_admin_privileges:
        raise PermissionDenied()

    receiver = submit.receiver
    review = submit.last_review
    data = {
        'submit': submit,
        'review': review,
        'user_has_admin_privileges': user_has_admin_privileges,
    }

    if receiver.show_submitted_file:
        with open(submit.file_path(), 'rb') as submitted_file:
            data['submitted_file'] = submitted_file.read().decode('utf-8', 'replace')

    if receiver.send_to_judge and review and review.protocol_exists():
        force_show_details = receiver.show_all_details or user_has_admin_privileges
        data['protocol'] = parse_protocol(review.protocol_path(), force_show_details)
        data['result'] = JudgeTestResult

    return render(request, 'submit/view_submit.html', data)


@login_required
def download_submit(request, submit_id):
    submit = get_object_or_404(Submit.objects.select_related('receiver'), pk=submit_id)
    if submit.user != request.user and not submit.receiver.has_admin_privileges(request.user):
        raise PermissionDenied()
    return send_file(request, submit.file_path(), submit.filename)


@login_required
def download_review(request, review_id):
    review = get_object_or_404(Review.objects.select_related('submit', 'submit__receiver'), pk=review_id)
    if review.submit.user != request.user and not review.submit.receiver.has_admin_privileges(request.user):
        raise PermissionDenied()
    return send_file(request, review.file_path(), review.filename)


@csrf_exempt
@require_POST
def receive_protocol(request):
    """
    Receive protocol from judge via POST and save it to review.protocol_path()
    """
    # judge expects submit_id, but at front-end it is Review that stores all feedback data
    review_id = request.POST['submit_id']
    review = get_object_or_404(Review, pk=review_id)
    protocol = request.POST['protocol'].encode('utf-8')
    write_chunks_to_file(review.protocol_path(), [protocol])

    protocol_data = parse_protocol(review.protocol_path())
    if protocol_data['ready']:
        review.score = protocol_data['score']
        review.short_response = protocol_data['final_result']
    else:
        review.short_response = ReviewResponse.PROTOCOL_CORRUPTED
    review.save()

    return HttpResponse("")


@api_view(['POST'])
@permission_classes([])
def external_submit(request):
    """
    Receive a request from an external application, create submit with review after validation.
    """
    serializer = ExternalSubmitSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated = serializer.validated_data

    receiver = SubmitReceiver.objects.get(token=validated['token'])
    if not receiver.allow_external_submits or not receiver.can_post_submit(validated['user']):
        raise PermissionDenied()

    submit = create_submit(user=validated['user'], receiver=receiver)
    submit.save()
    review = Review(submit=submit, score=validated['score'], short_response=ReviewResponse.OK)
    review.save()

    return APIResponse()
