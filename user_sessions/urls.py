from django.urls import path, include
from user_sessions import views
from django.conf.urls import url


urlpatterns = [
    path('signup/',views.CreateUserView.as_view(),name="Sign-Up"), 
    path('list/',views.ListUsersView.as_view(),name='List'),

    url(r'^session/(?P<mobile_number>\d+)$',
        views.ListClientSession.as_view(), name='session details'),
    url(r'^session/(?P<mobile_number>\d+)/v$',
        views.ListVerboseClientSessions.as_view(), name='verbose session details'),
    

]
