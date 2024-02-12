from django.urls import path
from .views import update_last_online

urlpatterns = [
    path("update_last_online/", update_last_online, name="update_last_online"),
]
