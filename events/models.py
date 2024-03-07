from django.db import models


class Events(models.Model):
    """Model of events"""

    title = models.CharField(max_length=128, verbose_name="Название")
    description = models.CharField(max_length=1024, verbose_name="Описание")
    poster = models.ImageField(
        upload_to="events_poster",
        default="events_poster/default.jpg",
        verbose_name="Постер",
    )
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(blank=True, verbose_name="Дата окончания")
    is_completed = models.BooleanField(default=False, verbose_name="Окончилось ли")

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return f"{self.title} {self.is_completed}"
