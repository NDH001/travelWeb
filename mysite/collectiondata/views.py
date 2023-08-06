from django.views.generic import View
from django.http import JsonResponse

from django.contrib.auth.models import User
from traveldata.models import Sights,Foods,Shops
from .models import UserFoodCollection,UserShopCollection,UserSightCollection

'''-------------------------------------------------------------------------------------------'''
# the overall modification e.g. add/delete item
class CollectionMod(View):

    #override this
    target_foreign_model = None
    target_collection_model = None
    
    def post(self,request,*args,**kwargs):
        if request.user.is_anonymous:
            return JsonResponse({'message':'login','redirect_url':'/accounts/login/'}) 

        self.user = request.user
        self.collection = self.get_collection(request)
        return None
    
    def get_collection(self,request):
        return self.target_foreign_model.objects.get(pk=request.POST.get('item'))
    
    def collection_exists(self):
        return self.target_collection_model.objects.filter(user=self.user,collection=self.collection).exists()
    
class CreateMod(CollectionMod):

    def post(self,request,*args,**kwargs):       

        # if a jsonresponse is returned which means the user is not logged in
        response = super().post(request,*args,**kwargs)
        if response:
            return response

        if self.collection_exists():
            return JsonResponse({'message':'target already in collection'})
        
        query = self.target_collection_model.objects.create(user=self.user,collection=self.collection)
        query.save()

        return JsonResponse({'message':'Added Collection'})

class DeleteMod(CollectionMod):
    
    def post(self,request,*args,**kwargs):
        # if a jsonresponse is returned which means the user is not logged in
        response = super().post(request,*args,**kwargs)
        if response:
            return response
        
        if not self.collection_exists():
            return JsonResponse({'message':'target does not exists in collection'})
        
        query = self.target_collection_model.objects.get(user=self.user,collection=self.collection)
        query.delete()

        return JsonResponse({'message':'Deleted Collection'})


class SightCreateMod(CreateMod):
    target_foreign_model = Sights
    target_collection_model= UserSightCollection

class FoodCreateMod(CreateMod):
    target_foreign_model = Foods
    target_collection_model= UserFoodCollection
        
class ShopCreateMod(CreateMod):
    target_foreign_model = Shops
    target_collection_model= UserShopCollection


class SightDeleteMod(DeleteMod):
    target_foreign_model = Sights
    target_collection_model= UserSightCollection

class FoodDeleteMod(DeleteMod):
    target_foreign_model = Foods
    target_collection_model= UserFoodCollection
        
class ShopDeleteMod(DeleteMod):
    target_foreign_model = Shops
    target_collection_model= UserShopCollection





        

