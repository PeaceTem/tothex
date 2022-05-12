from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PostAd(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField(upload_to='images/',  blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    clicks = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    relevance = models.FloatField(default=0)
    clickers = models.ManyToManyField(User, blank=True)

    detailpageviews = models.PositiveIntegerField(default=0)
    detailpageclicks = models.PositiveIntegerField(default=0)
    detailpagerelevance = models.FloatField(default=0)

    submitpageviews = models.PositiveIntegerField(default=0)
    submitpageclicks = models.PositiveIntegerField(default=0)
    submitpagerelevance = models.FloatField(default=0)

    bannerpageviews = models.PositiveIntegerField(default=0)
    bannerpageclicks = models.PositiveIntegerField(default=0)
    bannerpagerelevance = models.FloatField(default=0)

    correctionpageviews = models.PositiveIntegerField(default=0)
    correctionpageclicks = models.PositiveIntegerField(default=0)
    correctionpagerelevance = models.FloatField(default=0)


    def save(self, *args, **kwargs):
        if self.detailpageclicks > 0:
            self.detailpagerelevance = round(self.detailpageclicks/self.detailpageviews,2) 
        if self.submitpageclicks > 0:
            self.submitpagerelevance = round(self.submitpageclicks/self.submitpageviews,2) 
        if self.correctionpageclicks > 0:
            self.orrectionpagerelevance = round(self.correctionpageclicks/self.correctionpageviews,2) 

        if self.clicks > 0:
            self.relevance = round(self.clicks/self.views, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"