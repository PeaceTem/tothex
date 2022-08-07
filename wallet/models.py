from django.db import models
from core.models import Profile
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Wallet(models.Model):
    TYPES = (
        ('USD', _("USD")),
        ('NGN', _("NGN")),
        ('BTC', _("BTC")),
    )
    profile = models.OneToOneField(Profile, related_name='wallet', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2)
    wallet_type = models.CharField(choices=TYPES, max_length=100)
    last_paid_date = models.DateTimeField(null=True, blank=True)
    last_paid_amount = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.profile}"




class History(models.Model):
    TYPES = (
        ('USD', _("USD")),
        ('NGN', _("NGN")),
        ('BTC', _("BTC")),
    )
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='historys')
    text = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    incoming = models.BooleanField()
    value = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.CharField(choices=TYPES, max_length=20)

    def __str__(self):
        return f"{self.text}"