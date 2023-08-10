from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from traveldata.models import Sights, Foods, Shops

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
