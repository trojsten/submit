from django.conf.urls import url

from submit.commands import rejudge_submit
from submit.views import (download_review, download_submit, external_submit,
                          post_submit_form, receive_protocol, view_submit)

urlpatterns = [
    url(r'^post/(?P<receiver_id>\d+)/$', post_submit_form, name='post_submit'),
    url(r'^view/(?P<submit_id>\d+)/$', view_submit, name='view_submit'),
    url(r'^download/submit/(?P<submit_id>\d+)/$', download_submit, name='download_submit'),
    url(r'^download/review/(?P<review_id>\d+)/$', download_review, name='download_review'),
    url(r'^receive_protocol/$', receive_protocol),

    url(r'^commands/rejudge/submit/(?P<submit_id>\d+)/$', rejudge_submit, name='rejudge_submit'),

    # This the url path for this command is currently deactivated.
    # Also the button at submit_list template is hidden to prevent misclicks that could cause a judge overflow.
    # TODO: Implement pop-up / confirmation page for resubmit approval
    #url(r'^commands/rejudge/receiver/(?P<receiver_id>\d+)/$', rejudge_receiver_submits, name='rejudge_receiver_submits'),

    url(r'^ajax/external_submit/$', external_submit, name='external_submit'),
]
