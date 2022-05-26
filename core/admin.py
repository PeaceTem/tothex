from django.contrib import admin
from .models import Profile, Streak, Follower, Link, Interest, Device
# Register your models here.

admin.site.register(Profile)
admin.site.register(Streak)
admin.site.register(Follower)
admin.site.register(Link)
admin.site.register(Interest)
admin.site.register(Device)

