from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import related 
from django.db.models.signals import post_save 
from django.dispatch import receiver 
from django.contrib.auth.models import User


class Billing(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    address1 = models.CharField(max_length=200, null=True)
    address2 = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=200, null=True)
    city = models.CharField(default="", null=True, max_length=200)
    phone = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.username 

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = "Billing"

