from django.contrib import admin
from .models import TrueOrFalseQuestion, FourChoicesQuestion
# Register your models here.


admin.site.register(TrueOrFalseQuestion)
admin.site.register(FourChoicesQuestion)
