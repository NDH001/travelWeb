from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from journing.models import Comment
from traveldata.models import Sights
import random

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()

@receiver(post_save,sender=User)
def create_comment(sender,instance,created,**kwargs):
    arr = ['上海迪士尼度假区','东方明珠','外滩']
    comments = ['This is awesome!','Whoohoo','Highly recommended!','Would visit again!']
    if created:
        for _ in range (10):
            n = arr[random.randint(0,len(arr)-1)]
            s = comments[random.randint(0,len(arr)-1)]+n
            temp = Sights.objects.filter(name=n).first()
            Comment.objects.create(user=instance,sight=temp,comment=s,rating=random.randint(0,5))
