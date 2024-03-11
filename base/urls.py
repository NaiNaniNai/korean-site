from django.urls import path
from .views import update_last_online, IndexPageView

urlpatterns = [
    path("", IndexPageView.as_view(), name="index"),
    path("update_last_online/", update_last_online, name="update_last_online"),
]
