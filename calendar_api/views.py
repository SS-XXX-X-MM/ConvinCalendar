import code
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from httplib2 import Credentials, Response
from rest_framework.views import APIView
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import os.path

class GoogleCalendarInitAPIView(APIView):

    def get(self, request):
        if os.path.exists('client_secret.json'):
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                'client_secret.json',
                scopes=['https://www.googleapis.com/auth/calendar.events.readonly'],
                state="iamBatman"
                )
            
            flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect'

            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true')

            return HttpResponseRedirect(redirect_to=authorization_url)
        else:
            return JsonResponse({"Message":"Service Not Enabled"})

class GoogleCalendarRedirectAPIView(APIView):

    def get(self, request):
        try:
            auth_code = request.GET.get('code')
            if not auth_code:
                raise Exception("Auth Code NOT Found!")
        except Exception as e:
            return JsonResponse({"Message":e})

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/calendar.events.readonly'],
            state="iamBatman"
            )
        flow.redirect_uri = "http://localhost:8000/rest/v1/calendar/redirect"
        flow.fetch_token(code=auth_code)
        credentials = flow.credentials
        # print(credentials.token)



        try:
            service = build('calendar', 'v3', credentials=credentials)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])

        except HttpError as error:
            print('An error occurred: %s' % error)
        
        return JsonResponse({"Message":"Successful"})




