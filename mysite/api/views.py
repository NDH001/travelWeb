from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import PermissionDenied
from .serializers import (
    CitySerializer,
    ShopSerializer,
    FoodSerializer,
    SightSerializer,
    CommentSerializer,
)

from traveldata.models import Cities, Sights, Foods, Shops
from userdata.models import User
from journing.models import Comment


class GetData(APIView):
    model = None
    serializer_class = None

    def get(self, request, *args, **kwargs):
        if request.GET.get("q"):
            data = self.model.objects.filter(city=request.GET.get("q"))
        else:
            data = self.model.objects.all()[:100]
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data)


class GetCities(GetData):
    model = Cities
    serializer_class = CitySerializer

    def get(self, request, *args, **kwargs):
        if request.GET.get("q"):
            data = self.model.objects.get(city=request.GET.get("q"))
        else:
            data = self.model.objects.all()[:100]
        serializer = self.serializer_class(data, many=False)
        return Response(serializer.data)


class GetSights(GetData):
    model = Sights
    serializer_class = SightSerializer


class GetFoods(GetData):
    model = Foods
    serializer_class = FoodSerializer


class GetShops(GetData):
    model = Shops
    serializer_class = ShopSerializer


class ManipulateComments(APIView):
    def verify(self, request):
        key = request.META.get("HTTP_AUTHORIZATION").split("Bearer ")[1]
        if (
            key != "5134f4b0-f6d6-4cb0-9328-ad6f896bf086"
            and key != "3b7746d5-6e56-4f84-952a-ecf914b3487b"
        ):
            raise PermissionDenied("Not allowed")

        if key == "3b7746d5-6e56-4f84-952a-ecf914b3487b":
            self.user = User.objects.get(username="jun000222")
        elif key == "5134f4b0-f6d6-4cb0-9328-ad6f896bf086":
            self.user = User.objects.get(username="jun000333")

    def get(self, request, *args, **kwargs):
        self.verify(request)
        comments = Comment.objects.filter(user=self.user)

        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        self.verify(request)
        comment = Comment.objects.get(pk=request.data.get("id"))
        comment.comment = request.data.get("comment", comment.comment)
        comment.save()

        return Response("update success")

    def post(self, request, *args, **kwargs):
        self.verify(request)

        sight = Sights.objects.get(id=str(request.POST.get("place")).strip())
        comment = Comment.objects.create(
            user=self.user,
            sight=sight,
            rating=request.POST.get("rating"),
            comment=request.POST.get("comment"),
        )
        comment.save()
        return Response("create success")

    def delete(self, request, *args, **kwargs):
        self.verify(request)

        comment = Comment.objects.get(pk=request.data.get("id"))
        comment.delete()

        return Response("delete success")
