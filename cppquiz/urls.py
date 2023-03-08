from django.conf.urls import include, re_path
from django.views.generic.base import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/v1/quiz/', include('quiz.apiurls')),
    re_path(r'', include('quiz.urls')),
    re_path(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
]
