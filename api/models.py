import uuid
from django.db import models


from MMVS.settings import VIDEO_PATH


class VideoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=VIDEO_PATH)
    processing = models.BooleanField(default=False)
    processingSuccess = models.BooleanField(null=True, blank=True)
