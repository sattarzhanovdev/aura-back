from django.urls import path

from .callback_views import KieCallbackView

urlpatterns = [
    path("<str:callback_token>/", KieCallbackView.as_view(), name="kie-callback"),
]
