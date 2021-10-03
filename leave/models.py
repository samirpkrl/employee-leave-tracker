from django.db import models
from django.contrib.auth.models import User
from datetime import date
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Empleave(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=128)
    entry_date=models.DateField(auto_now_add=True,null=True)
    from_date = models.DateField()
    to_date = models.DateField()
    reason= models.TextField(max_length=256,null = True,blank = True)
    days=models.IntegerField(null=True,blank=True)
        
    def __str__(self):
        return self.title

    def date_difference(self):
        delta = self.to_date - self.from_date
        return (delta.days+1)

@receiver(post_save, sender=Empleave, dispatch_uid="update_leave_days")
def update_days(sender, instance, created, **kwargs):
    if created:
        delta = instance.to_date - instance.from_date
        tot=delta.days+1
        instance.days = tot
        instance.save()