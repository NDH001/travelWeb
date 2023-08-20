from django.db import models
from django.contrib.auth.models import User
from traveldata.models import Cities
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.BooleanField(choices=[(0, "Female"), (1, "Male")], default=False)
    profile_pic = models.ImageField(default="default.jpg", upload_to="profile_pics")
    shared = models.PositiveIntegerField(
        default=0, verbose_name="Journal shared", editable=False
    )
    city = models.ForeignKey(Cities, null=True, blank=True, on_delete=models.CASCADE)
    desc = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="personal statement",
        default="Write some details about yourself",
    )
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.profile_pic.path)
    #     if img.height > 300 or img.width > 300:
    #         img.thumbnail((300, 300))
    #         img.save(self.profile_pic.path)

    class Meta:
        db_table = '"userdata"."profile"'


class Connection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="follower"
    )
    followed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User:{str(self.user)} Follower:{str(self.follower)}"

    class Meta:
        db_table = '"userdata"."connection"'
        ordering = ["-followed_on"]
