from django.urls import path

from . import views
from .smsview import send_text_message
from . import sms_webhook


urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>/", views.details, name="details"),
    path("create", views.create_restaurant, name="create_restaurant"),
    path("add", views.add_restaurant, name="add_restaurant"),
    path("review/<int:id>", views.add_review, name="add_review"),
    path("send-text-message/", send_text_message, name="send_text_message"),
    path("sms_webhook/", sms_webhook.sms_webhook, name="sms_webhook"),
]
