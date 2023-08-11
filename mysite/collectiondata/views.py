from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.models import User

from traveldata.models import Sights, Foods, Shops
from .models import UserFoodCollection, UserShopCollection, UserSightCollection
from journing.decorator import ajax_check_login

"""-------------------------------------------------------------------------------------------"""


# the overall modification e.g. add/delete item
class CollectionMod(View):
    # override this
    target_foreign_model = None
    target_collection_model = None

    @ajax_check_login
    def post(self, request, *args, **kwargs):
        self.collection = self.target_foreign_model.objects.get(
            pk=request.POST.get("item")
        )

    def collection_exists(self):
        return self.target_collection_model.objects.filter(
            user=self.user, collection=self.collection
        ).exists()


# the class that handles create activities for all models,e.g. sight,shop,food
class CreateMod(CollectionMod):
    @ajax_check_login
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if self.collection_exists():
            return JsonResponse({"message": "target already in collection"})

        query = self.target_collection_model.objects.create(
            user=self.user, collection=self.collection
        )
        query.save()

        return JsonResponse({"message": "Added Collection"})


# the class that handles delete activities for all models,e.g. sight,shop,food
class DeleteMod(CollectionMod):
    @ajax_check_login
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if not self.collection_exists():
            return JsonResponse({"message": "target does not exists in collection"})

        query = self.target_collection_model.objects.get(
            user=self.user, collection=self.collection
        )
        query.delete()

        return JsonResponse({"message": "Deleted Collection"})


# inherited classes that handles different categories activities
class SightCreateMod(CreateMod):
    target_foreign_model = Sights
    target_collection_model = UserSightCollection


class FoodCreateMod(CreateMod):
    target_foreign_model = Foods
    target_collection_model = UserFoodCollection


class ShopCreateMod(CreateMod):
    target_foreign_model = Shops
    target_collection_model = UserShopCollection


class SightDeleteMod(DeleteMod):
    target_foreign_model = Sights
    target_collection_model = UserSightCollection


class FoodDeleteMod(DeleteMod):
    target_foreign_model = Foods
    target_collection_model = UserFoodCollection


class ShopDeleteMod(DeleteMod):
    target_foreign_model = Shops
    target_collection_model = UserShopCollection
