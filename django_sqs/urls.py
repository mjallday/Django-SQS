from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('django_sqs.views',
    url(r'^$', 'dashboard', name='django_sqs_stats'),
)
