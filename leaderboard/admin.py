from django.contrib import admin
from .models import CoinsEarnerLeaderBoard, CreatorLeaderBoard, ReferralLeaderBoard
# Register your models here.
admin.site.register(CoinsEarnerLeaderBoard)
admin.site.register(CreatorLeaderBoard)
admin.site.register(ReferralLeaderBoard)