from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "collectiondata"
urlpatterns = [
    # -----------------------------------------------------------------------------------------------------#
    path("sights/create/<str:pk>/", views.SightCreateMod.as_view(), name="add_sight"),
    path(
        "sights/delete/<str:pk>/", views.SightDeleteMod.as_view(), name="delete_sight"
    ),
    path("foods/create/<str:pk>/", views.FoodCreateMod.as_view(), name="add_food"),
    path("foods/delete/<str:pk>/", views.FoodDeleteMod.as_view(), name="delete_food"),
    path("shops/create/<str:pk>/", views.ShopCreateMod.as_view(), name="add_shop"),
    path("shops/delete/<str:pk>/", views.ShopDeleteMod.as_view(), name="delete_shop"),
]
