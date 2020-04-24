from django.conf.urls import include, url
from django.views.generic.base import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/quiz/', include('cppquiz.quiz.apiurls')),
    url(r'', include('cppquiz.quiz.urls')),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
]
