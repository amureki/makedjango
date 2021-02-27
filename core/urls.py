from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain",
        ),
    ),
    path(
        "humans.txt",
        TemplateView.as_view(
            template_name="humans.txt",
            content_type="text/plain",
        ),
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
