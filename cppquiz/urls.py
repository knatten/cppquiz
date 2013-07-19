from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cppquiz.views.home', name='home'),
    # url(r'^cppquiz/', include('cppquiz.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('cppquiz.quiz.urls', namespace='quiz')),
    (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
)
