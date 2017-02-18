from django import forms
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from submit import settings as submit_settings
from submit.models import Review, Submit, SubmitReceiver


class SubmitReceiverAdminForm(forms.ModelForm):
    """
    Adds a checkbox to SubmitReceiverAdmin -- when this checkbox is checked, a new token will be generated.
    This may be useful if a token leaks.
    """
    regenerate_token = forms.BooleanField(required=False)

    def save(self, commit=True):
        instance = super(SubmitReceiverAdminForm, self).save(commit)
        if self.cleaned_data.get('regenerate_token', False):
            instance.token = SubmitReceiver.generate_token()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = SubmitReceiver
        fields = '__all__'


class SubmitReceiverAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'task')
    search_fields = ('task__name', )

    readonly_fields = ('token', )
    form = SubmitReceiverAdminForm
    fieldsets = (
        (None, {
            'fields': ('task', )
        }),
        ('Form options', {
            'fields': ('has_form', 'caption', 'extensions', 'languages'),
        }),
        ('External submits options', {
            'fields': ('external_link', ('allow_external_submits', 'regenerate_token'), 'token'),
        }),
        ('Judge options', {
            'fields': ('send_to_judge', 'inputs_folder_at_judge'),
        }),
        ('Submit page options', {
            'fields': ('show_all_details', 'show_submitted_file'),
        }),
    )


class ReceiverFromTemplateForm(forms.ModelForm):
    receiver_template = forms.ChoiceField(
        choices=[(None, '')] + [(k, k) for k in submit_settings.SUBMIT_RECEIVER_TEMPLATES.keys()],
        required=False,
        label='Submit receiver template',
        help_text=_('Basic receiver settings will be set based on selected type. For advanced settings click "Change".'
                    '<br />(When adding a new receiver, click "Save and continue editing" first.)')
    )

    class Meta:
        model = SubmitReceiver
        fields = '__all__'
        widgets = {field.name: forms.HiddenInput() for field in SubmitReceiver._meta.get_fields()}

    def clean(self):
        cleaned_data = super(ReceiverFromTemplateForm, self).clean()
        template = self.cleaned_data.get('receiver_template', None)
        if template:
            cleaned_data.update(submit_settings.SUBMIT_RECEIVER_TEMPLATES[template])
        return cleaned_data


class SubmitReceiverFromTemplateInline(admin.StackedInline):
    """
    This inline admin consists of only one choice field - receiver_template - for a submit receiver.
    When a template is selected, fields of receiver will be filled with data from
    `submit_settings.SUBMIT_RECEIVER_TEMPLATES` after save.
    """
    model = SubmitReceiver
    extra = 0
    show_change_link = True
    exclude = ('token',)
    form = ReceiverFromTemplateForm


class SubmitReceiverFullInline(admin.TabularInline):
    """
    This inline admin compactly provides almost all receiver settings.
    """
    model = SubmitReceiver
    extra = 0
    show_change_link = True
    exclude = ('token', )
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '15'})},
    }


class ReviewInline(admin.StackedInline):
    model = Review
    fields = ('time', 'score', 'short_response', 'comment', 'filename')
    readonly_fields = ('time',)
    ordering = ('-time',)
    extra = 0


class ViewOnSiteMixin(object):
    """
    Provides one column for ModelAdmin list display. This column will contain links to web pages of model instances.
    This serves as shortcut: to get to the instance web page, only one click is now necessary instead of two clicks
    (List view -> Model change view -> Instance web page).
    """
    def view_on_site_list_display(self, obj):
        return mark_safe(u'<a href="{}">{}</a>'.format(obj.get_absolute_url(), 'view on site'))
    view_on_site_list_display.allow_tags = True
    view_on_site_list_display.short_description = u'View on site'


class SubmitAdmin(ViewOnSiteMixin, admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = ('submit_id', 'view_on_site_list_display', 'user', 'task', 'receiver', 'status', 'score', 'time',
                    'is_accepted',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'receiver__task__name',)
    list_filter = ('is_accepted', 'user__is_staff',)

    def get_queryset(self, request):
        qs = self.model.with_reviews.get_queryset().select_related('receiver__task', 'user')

        # needed from superclass method
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def submit_id(self, submit):
        return 'submit %d' % (submit.id,)
    submit_id.admin_order_field = 'id'

    def task(self, submit):
        return submit.receiver.task
    task.admin_order_field = 'receiver__task'

    def status(self, submit):
        review = submit.last_review
        return review.short_response if review is not None else ''

    def score(self, submit):
        review = submit.last_review
        return review.display_score() if review is not None else ''


admin.site.register(SubmitReceiver, SubmitReceiverAdmin)
admin.site.register(Submit, SubmitAdmin)
