from django.db import models

# Create your models here.

# {
#   "kind": "calendar#events",
#   "etag": etag,
#   "summary": string,
#   "description": string,
#   "updated": datetime,
#   "timeZone": string,
#   "accessRole": string,
#   "defaultReminders": [
#     {
#       "method": string,
#       "minutes": integer
#     }
#   ],
#   "nextPageToken": string,
#   "nextSyncToken": string,
#   "items": [
#     events Resource
#   ]
# }

class Event(models.Model):
    kind = models.CharField()
    etag = models.CharField()
    summary = models.CharField()
    description = models.CharField()
    updated = models.DateTimeField()
    time_zone = models.CharField()
    access_role = models.CharField()
    next_page_token = models.CharField()
    next_sync_token = models.CharField()
    default_reminder_method = models.CharField()
    default_reminder_minutes = models.IntegerField()

    def __str__(self) -> str:
        return self.description



