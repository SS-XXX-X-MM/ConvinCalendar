from django.shortcuts import render
from rest_framework.views import APIView
import google.oauth2.credentials
import google_auth_oauthlib.flow
# Create your views here.

class GoogleCalendarInitAPIView(APIView):

    def post(self, request):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly']
            )
        
        flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect'

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')

        print(authorization_url)

class GoogleCalendarRedirectAPIView(APIView):

    def get(self, request):
        pass


