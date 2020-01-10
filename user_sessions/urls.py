from django.urls import path, include
from user_sessions import views
from django.conf.urls import url


urlpatterns = [
    path('signup/',views.CreateUserView.as_view(),name="Sign_Up"), 
    path('list/',views.ListUsersView.as_view(),name='list'),

    url(r'^session/(?P<mobile_number>\d+)$',
        views.ListClientSession.as_view(), name='session_details'),
    url(r'^session/(?P<mobile_number>\d+)/v$',
        views.ListVerboseClientSessions.as_view(), name='verbose_session_details'),
    

]
