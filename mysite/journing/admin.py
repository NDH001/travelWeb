from django.contrib import admin
from django.contrib.auth.models import User
from userdata.models import Profile
from .models import Comment

admin.site.register(Profile)

admin.site.register(Comment)
