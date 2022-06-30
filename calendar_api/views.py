from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.views import APIView
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
import os.path

class GoogleCalendarInitAPIView(APIView):
    SCOPE = ['https://www.googleapis.com/auth/calendar.events.readonly']
    REDIRECT_URI = 'http://localhost:8000/rest/v1/calendar/redirect'
    STATE = 'iamBatman'

    def get(self, request):
        """
        GET THE AUTHORIZATION URL FOR LOGGING IN ACCOUNT AND PROVIDING CONSENT
        REDIRECTS TO: GoogleCalendarRedirectAPIView
        """
        
        if os.path.exists('client_secret.json'):
            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                'client_secret.json',
                scopes = self.SCOPE,
                state = self.STATE
                )
            
            flow.redirect_uri = self.REDIRECT_URI

            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true')

            return HttpResponseRedirect(redirect_to=authorization_url)
        else:
            return JsonResponse({"Message":"Service Not Enabled"})



class GoogleCalendarRedirectAPIView(APIView):
    SCOPE = ['https://www.googleapis.com/auth/calendar.events.readonly']
    REDIRECT_URI = 'http://localhost:8000/rest/v1/calendar/redirect'
    STATE = 'Iambatman'

    def get(self, request):
        """
        GET: AUTHORIZATION_CODE OR ERROR
        EXTRACT: ACCESS_TOKEN
        INVOKE THE DESIRED GOOGLE API 
        """
        try:
            auth_code = request.GET.get('code')
            if not auth_code:
                raise Exception("Auth Code NOT Found!")

            flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=self.SCOPE,
            state=self.STATE
            )

            flow.redirect_uri = self.REDIRECT_URI
            flow.fetch_token(code=auth_code)
            credentials = flow.credentials
            if not credentials:
                raise Exception("Access Token NOT Found!")
            # print(credentials.token)

        except Exception as e:
            return JsonResponse({"Message":e})


        #  GET THE CALENDAR SERVICE AND INVOKE API ENDPOINTS IN SCOPE
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
                return JsonResponse({"Message":"No Upcoming Events"})

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
            return JsonResponse({"Message":"Successful"})

        except HttpError as error:
            return JsonResponse({"Message":error})




