from django.db import models

# Create your models here.



class Request(models.Model):
    requests = models.PositiveIntegerField(default=0)
   
    def __str__(self):
        return f"<Request: {self.requests}>" 



class ViewRequest(models.Model):
    name = models.CharField(max_length=100)
    requests = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"<ViewRequest: {self.name}>"


class CountryRequest(models.Model):
    name = models.CharField(max_length=100)
    requests = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"<CountryRequest: {self.name}>"

