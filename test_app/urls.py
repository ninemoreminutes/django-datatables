from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('test_app.views',
    url(r'^$', 'index', name='index'),
)
