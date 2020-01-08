from django.urls import path, include
from user_sessions import views

urlpatterns = [
    path('user-signup/',views.CreateUserView.as_view(),name="Sign-Up"), 

]
