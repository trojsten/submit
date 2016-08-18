from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.static import serve

import example.tasks.urls
import submit.urls

urlpatterns = [
    url(r'^$', lambda r: HttpResponseRedirect(reverse('task_list'))),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tasks/', include(example.tasks.urls)),
    url(r'^submit/', include(submit.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
