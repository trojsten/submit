from django.contrib import admin
from django.utils.safestring import mark_safe

from submit.models import SubmitReceiver, Submit, Review


class SubmitReceiverAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'task')
    search_fields = ('task__name', )


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
