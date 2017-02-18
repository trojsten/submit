import binascii
import os

from django.conf import settings as django_settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.query import Prefetch
from django.utils.encoding import python_2_unicode_compatible
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from submit import settings as submit_settings
from submit import constants


class BaseTask(models.Model):
    """
    Base model for Task to be extended in outer app using submit app.
    Defines interface required by submit app.
    """
    name = models.CharField(max_length=128)

    def get_absolute_url(self):
        raise NotImplementedError

    class Meta:
        abstract = True


def comma_separated_string_to_list(comma_string):
    if comma_string.strip() == '':
        return []
    return [word.strip() for word in comma_string.split(',')]


def validate_languages(value):
    for lang in comma_separated_string_to_list(value):
        if lang not in constants.LANGUAGE_IDENTIFIERS:
            raise ValidationError(_('Language "%(lang)s" is not supported by judge.'), params={'lang': lang})


@python_2_unicode_compatible
class SubmitReceiver(models.Model):
    """
    Submit receiver manages one type of submits for one task.
    """
    task = models.ForeignKey(submit_settings.SUBMIT_TASK_MODEL)

    has_form = models.BooleanField(default=False, help_text=_('Check to collect files via submit form.'))
    caption = models.CharField(max_length=128, blank=True, default='',
                               help_text=_('Text that appears on the left from submit form.'))
    extensions = models.CharField(max_length=256, blank=True, default='', help_text=_(
        'List of comma separated extensions e.g. "txt, pdf, doc".<br />'
        'Leave blank to accept any extension.'))
    languages = models.CharField(max_length=256, blank=True, default='', validators=[validate_languages], help_text=_(
        'List of comma separated programming language extensions e.g. "c, cc, py, hs".<br />'
        'Use languages supported by the judge from: %(languages)s.<br />'
        'When languages are set, field "extensions" is ignored.'
        ) % {'languages': ', '.join(constants.LANGUAGE_IDENTIFIERS)})

    external_link = models.CharField(max_length=256, blank=True, default='', help_text=_(
        'URL for external submits. A button with link will be rendered in the submit form.'))
    allow_external_submits = models.BooleanField(default=False)
    token = models.CharField(verbose_name='token', max_length=64, unique=True, blank=True, help_text=_(
        'Secret key allowing external submits via API, will be generated automatically.'))

    send_to_judge = models.BooleanField(default=False, help_text=_('Check to send submits to automated judge.'))
    inputs_folder_at_judge = models.CharField(max_length=128, blank=True, default='',  help_text=_(
        'If left blank, and send_to_judge is checked, this field will be set automatically.'))

    show_all_details = models.BooleanField(default=False, help_text=_('Check to display protocol details to all users.'))
    show_submitted_file = models.BooleanField(default=False, help_text=_(
        'Check to render submitted file as a part of web page for submit.'))

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()

        if not self.inputs_folder_at_judge and self.send_to_judge:
            self.inputs_folder_at_judge = import_string(submit_settings.JUDGE_DEFAULT_INPUTS_FOLDER_FOR_RECEIVER)(self)

        super(SubmitReceiver, self).save(*args, **kwargs)

    @staticmethod
    def generate_token():
        return binascii.hexlify(os.urandom(20)).decode()

    def get_languages(self):
        return comma_separated_string_to_list(self.languages)

    def get_extensions(self):
        return ['.' + e for e in comma_separated_string_to_list(self.extensions)]

    class Meta:
        verbose_name = 'submit receiver'
        verbose_name_plural = 'submit receivers'

    def can_post_submit(self, user):
        return import_string(submit_settings.SUBMIT_CAN_POST_SUBMIT)(self, user)

    def has_admin_privileges(self, user):
        return import_string(submit_settings.SUBMIT_HAS_ADMIN_PRIVILEGES_FOR_RECEIVER)(self, user)

    def __str__(self):
        return import_string(submit_settings.SUBMIT_DISPLAY_SUBMIT_RECEIVER_NAME)(self)


class SubmitWithReviewManager(models.Manager):
    def get_queryset(self):
        submit_qs = super(SubmitWithReviewManager, self).get_queryset()

        reviews_qs = Review.objects \
            .filter(submit__in=submit_qs) \
            .order_by('-submit__time', '-submit__pk', '-time', '-pk') \
            .distinct('submit__time', 'submit__pk') \

        return submit_qs.prefetch_related(Prefetch('review_set', queryset=reviews_qs, to_attr='last_reviews_list'))


@python_2_unicode_compatible
class Submit(models.Model):
    """
    Submit holds information about user-submitted data.
    """
    receiver = models.ForeignKey(SubmitReceiver)
    user = models.ForeignKey(django_settings.AUTH_USER_MODEL)
    time = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=128, blank=True)

    NOT_ACCEPTED = 0
    ACCEPTED_WITH_PENALIZATION = 1
    ACCEPTED = 2
    IS_ACCEPTED_CHOICES = [
        (NOT_ACCEPTED, _('no')),
        (ACCEPTED_WITH_PENALIZATION, _('with penalization')),
        (ACCEPTED, _('yes')),
    ]
    is_accepted = models.IntegerField(default=ACCEPTED, choices=IS_ACCEPTED_CHOICES)

    objects = models.Manager()
    with_reviews = SubmitWithReviewManager()

    def dir_path(self):
        """
        All files related to this submit are stored here: submitted file, review files, testing protocols, raw files.
        Each submit has a dedicated location for its files in
        /settings.SUBMIT_PATH/submits/<user_id>/<receiver_id>/<submit_id>/
        """
        return os.path.join(submit_settings.SUBMIT_PATH, 'submits',
                            str(self.user.id), str(self.receiver.id), str(self.id))

    def file_path(self):
        """
        Submit can hold one file. The original filename is stored in submit.filename
        Because of the filename id.submit, files with inappropriate names (e.g. 12345.review) will be stored correctly.
        """
        return os.path.join(self.dir_path(), str(self.id) + constants.SUBMITTED_FILE_EXTENSION)

    def file_exists(self):
        return os.path.exists(self.file_path())

    def get_last_review(self):
        if hasattr(self, 'last_reviews_list'):
            return self.last_reviews_list[0] if len(self.last_reviews_list) > 0 else None
        return self.review_set.order_by('-time', '-pk').first()
    last_review = property(get_last_review)

    def get_absolute_url(self):
        return reverse('submit.views.view_submit', kwargs=dict(submit_id=self.id))

    class Meta:
        verbose_name = 'submit'
        verbose_name_plural = 'submits'

    def __str__(self):
        return 'submit %d (%s, %s, %s)' % (
            self.id,
            self.user,
            self.receiver,
            self.time.strftime('%H:%M:%S %d.%m.%Y'),
        )


class ReviewManager(models.Manager):
    def get_queryset(self):
        qs = super(ReviewManager, self).get_queryset()
        return import_string(submit_settings.SUBMIT_PREFETCH_DATA_FOR_SCORE_CALCULATION)(qs)


@python_2_unicode_compatible
class Review(models.Model):
    """
    Review holds information about feedback for one submit. This feedback can be created manually or automatically.

    `review.score` is an absolute scoring, its semantics (how this number affects the results) should be defined
    in a result-app

    Review file should store file with feedback (e.g. submitted file with reviewer's comments).
    `review.filename` is an original name of this file.
    """
    submit = models.ForeignKey(Submit)
    score = models.DecimalField(max_digits=10, decimal_places=5)
    time = models.DateTimeField(auto_now_add=True)
    short_response = models.CharField(max_length=128, blank=True,
                                      choices=constants.ReviewResponse.all_items_as_choices())
    comment = models.TextField(blank=True)
    filename = models.CharField(max_length=128, blank=True)

    objects = ReviewManager()

    def display_score(self):
        return import_string(submit_settings.SUBMIT_DISPLAY_SCORE)(self)

    def render_comment(self):
        return import_string(submit_settings.SUBMIT_RENDER_REVIEW_COMMENT)(self)

    def verbose_response(self):
        return constants.ReviewResponse.verbose(self.short_response)

    def file_path(self):
        return os.path.join(self.submit.dir_path(), str(self.id) + constants.REVIEWED_FILE_EXTENSION)

    def file_exists(self):
        return os.path.exists(self.file_path())

    def raw_path(self):
        return os.path.join(self.submit.dir_path(), str(self.id) + constants.TESTING_RAW_EXTENSION)

    def protocol_path(self):
        return os.path.join(self.submit.dir_path(), str(self.id) + constants.TESTING_PROTOCOL_EXTENSION)

    def protocol_exists(self):
        return os.path.exists(self.protocol_path())

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'

    def __str__(self):
        return 'review %d for %s' % (self.id, str(self.submit))
