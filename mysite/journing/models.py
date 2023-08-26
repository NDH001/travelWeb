from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from traveldata.models import Sights, Foods, Shops, Cities


# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sight = models.ForeignKey(Sights, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000, default="Awesome place!")
    rating = models.SmallIntegerField(default=2)
    created_on = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return str(self.user) + " " + str(self.comment)

    def get_absolute_url_sight(self):
        return reverse(
            "journing:sights_comments",
            kwargs={"pk": self.sight.pk, "slug": self.sight.slug},
        )

    class Meta:
        db_table = '"journingdata"."comments"'
        ordering = ["-created_on"]


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=50, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.message)

    class Meta:
        db_table = '"journingdata"."noti"'


class Journal(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    title = models.CharField(default="Untitled")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + " " + str(self.created_on)

    class Meta:
        db_table = '"journingdata"."journal"'
        ordering = ["created_on"]


class Record(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_uuid = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_uuid")
    hour = models.SmallIntegerField(default=None)
    remark = models.CharField(max_length=1000, default=None)
    date = models.DateField(default=None, null=True)
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.content_object) + " " + str(self.date)

    @property
    def activity_name(self):
        return str(self.content_object) if self.content_object else None

    @property
    def list_name(self):
        if isinstance(self.content_object, Sights):
            return "sight_collections"

        if isinstance(self.content_object, Foods):
            return "food_collections"

        return "shop_collections"

    @property
    def image(self):
        return self.content_object.img_local

    class Meta:
        db_table = '"journingdata"."record"'
