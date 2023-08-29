from django.urls import path
from . import views

urlpatterns = [
    path("cities/", views.GetCities.as_view(), name="api_get_cities"),
    path("sights/", views.GetSights.as_view(), name="api_get_sights"),
    path("foods/", views.GetFoods.as_view(), name="api_get_foods"),
    path("shops/", views.GetShops.as_view(), name="api_get_shops"),
    path("comments/", views.ManipulateComments.as_view(), name="api_mani_comments"),
]
