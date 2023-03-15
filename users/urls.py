from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    # Add other paths for your app's views here
]
