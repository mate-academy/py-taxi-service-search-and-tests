from django.urls import path

from .views import register

urlpatterns = [
    path("register/", register, name="signup")
]

app_name = "register"
