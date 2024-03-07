from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from events.models import Events


class EventsAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Events
        fields = "__all__"


# Register your models here.
@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    form = EventsAdminForm
    list_display = ("title", "start_date", "end_date", "is_completed")
    list_display_links = ("title",)
