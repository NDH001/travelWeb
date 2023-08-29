from rest_framework.serializers import ModelSerializer
from traveldata.models import Cities, Sights, Foods, Shops
from journing.models import Comment


class CitySerializer(ModelSerializer):
    class Meta:
        model = Cities
        fields = "__all__"


class SightSerializer(ModelSerializer):
    class Meta:
        model = Sights
        fields = "__all__"


class FoodSerializer(ModelSerializer):
    class Meta:
        model = Foods
        fields = "__all__"


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shops
        fields = "__all__"


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shops
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
