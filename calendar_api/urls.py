import imp
from django.urls import path
from .views import GoogleCalendarInitAPIView, GoogleCalendarRedirectAPIView

urlpatterns = [
    path('init/', GoogleCalendarInitAPIView().as_view(), name="calendar_init"),
    path('redirect/', GoogleCalendarRedirectAPIView().as_view(), name="calendar_redirect"),
]
