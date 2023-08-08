from django.db import models
from django.contrib.auth.models import User

from traveldata.models import Sights, Foods, Shops


# Create three models that act as a bridge model for the many to many relationship between user and collections
class UserSightCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.ForeignKey(Sights, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " " + str(self.collection)

    class Meta:
        db_table = '"collectiondata"."sight_collection"'


class UserFoodCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.ForeignKey(Foods, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " " + str(self.collection)

    class Meta:
        db_table = '"collectiondata"."food_collection"'


class UserShopCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.ForeignKey(Shops, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + " " + str(self.collection)

    class Meta:
        db_table = '"collectiondata"."shop_collection"'
