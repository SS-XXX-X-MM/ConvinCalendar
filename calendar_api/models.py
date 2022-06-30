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
    kind = models.CharField(max_length=100)
    etag = models.CharField(max_length=100)
    summary = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    updated = models.DateTimeField()
    time_zone = models.CharField(max_length=100)
    access_role = models.CharField(max_length=100)
    next_page_token = models.CharField(max_length=100)
    next_sync_token = models.CharField(max_length=100)
    default_reminder_method = models.CharField(max_length=100)
    default_reminder_minutes = models.IntegerField()

    def __str__(self) -> str:
        return self.description



