from django.urls import path

from .views import CustomLoginView, CustomLogoutView, CustomPasswordChangeView

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("change_password/", CustomPasswordChangeView.as_view(), name="change_password"),
]
