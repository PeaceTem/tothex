from django.contrib import admin
from .models import StreakLeaderBoard, CoinsEarnerLeaderBoard, CreatorLeaderBoard, ReferralLeaderBoard
# Register your models here.
admin.site.register(StreakLeaderBoard)
admin.site.register(CoinsEarnerLeaderBoard)
admin.site.register(CreatorLeaderBoard)
admin.site.register(ReferralLeaderBoard)