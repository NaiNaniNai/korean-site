from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone


class MyBackend(ModelBackend):
    def get_user(self, user_id):
        try:
            user = get_user_model().objects.get(pk=user_id)
            user.last_online = timezone.now()
            user.save(update_fields=["last_online"])
            return user
        except get_user_model().DoesNotExist:
            return None
