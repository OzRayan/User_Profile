from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'sign_in/$', views.sign_in, name='sign_in'),
    url(r'sign_up/$', views.sign_up, name='sign_up'),
    url(r'sign_out/$', views.sign_out, name='sign_out'),
    url(r'profile/detail/$', views.detail_view, name='profile_detail'),
    url(r'profile/edit/$', views.edit_view, name='profile_edit'),
    url(r'profile/password/$', views.password_view, name='password_edit'),
]
