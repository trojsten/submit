from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from submit.models import SubmitReceiverTemplate, SubmitReceiver, Submit, Review


class SubmitReceiverTemplateAdmin(admin.ModelAdmin):
    pass


class LoadConfigurationFromTemplate(forms.Select):
    class Media:
        js = ('submit/load-configuration-from-template.js', )


class SubmitReceiverForm(forms.ModelForm):
    receiver_template = forms.ChoiceField(
        choices=[],
        widget=LoadConfigurationFromTemplate()
    )

    def __init__(self, *args, **kwargs):
        super(SubmitReceiverForm, self).__init__(*args, **kwargs)
        self.fields['receiver_template'].choices = ((x.id, str(x)) for x in SubmitReceiverTemplate.objects.all())

    class Meta:
        model = SubmitReceiver
        fields = ('task', 'receiver_template', 'configuration')
        widgets = {
            'configuration': forms.Textarea(attrs={'rows': 15, 'cols': 50})
        }


class SubmitReceiverAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'task')
    form = SubmitReceiverForm


class ReviewInline(admin.StackedInline):
    model = Review
    fields = ('time', 'score', 'short_response', 'comment', 'filename')
    readonly_fields = ('time',)
    ordering = ('-time',)
    extra = 0


class ViewOnSiteMixin(object):
    def view_on_site_list_display(self, obj):
        return mark_safe(u'<a href="{}">{}</a>'.format(obj.get_absolute_url(), 'view on site'))
    view_on_site_list_display.allow_tags = True
    view_on_site_list_display.short_description = u'View on site'


class SubmitAdmin(ViewOnSiteMixin, admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = ('submit_id', 'view_on_site_list_display', 'receiver', 'user', 'status', 'score', 'time',
                    'is_accepted')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

    def get_queryset(self, request):
        qs = self.model.with_reviews.get_queryset()

        # needed from superclass method
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def submit_id(self, submit):
        return 'submit %d' % (submit.id,)
    submit_id.admin_order_field = 'id'

    def status(self, submit):
        review = submit.last_review
        return review.short_response if review is not None else ''

    def score(self, submit):
        review = submit.last_review
        return review.display_score() if review is not None else ''


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'time', 'short_response', 'display_score', 'submit_id_', 'submit_user',
                    'submit_receiver', 'submit_time',)

    def get_queryset(self, request):
        return super(ReviewAdmin, self).get_queryset(request).select_related('submit__user')

    def review_id(self, review):
        return 'review %d' % (review.id,)
    review_id.admin_order_field = 'id'

    def submit_id_(self, review):
        return '%d' % (review.submit.id, )
    submit_id_.admin_order_field = 'submit__id'

    def submit_user(self, review):
        return review.submit.user
    submit_user.admin_order_field = 'submit__user'

    def submit_receiver(self, review):
        return review.submit.receiver

    def submit_time(self, review):
        return review.submit.time
    submit_user.admin_order_field = 'submit__time'


admin.site.register(SubmitReceiverTemplate, SubmitReceiverTemplateAdmin)
admin.site.register(SubmitReceiver, SubmitReceiverAdmin)
admin.site.register(Submit, SubmitAdmin)
admin.site.register(Review, ReviewAdmin)
