# urls.py

from django.urls import path

from .views import LoggedInUserView

urlpatterns = [
    path('user/', LoggedInUserView.as_view(), name='users'), 
]
