from django.db import models

# A shorten url
class Url(models.Model):
    url_id = models.CharField("The short url id", max_length=8)
    orig_url = models.TextField("Original url")
    created_at = models.DateTimeField("Created at")
    clicks = models.IntegerField(default=0)