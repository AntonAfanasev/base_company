from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.profiles_filter, name='profiles_filter'),
    #url(r'^(?P<pk>[0-9]+)/$', views.profile_info, name='profile_info'),
    url(r'^$', views.ProfilesFilter.as_view(), name='profiles_filter'),
    url(r'^(?P<pk>[0-9]+)/$', views.ProfileInfo.as_view(), name='profile_info'),
]
