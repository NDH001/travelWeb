from typing import Any, Dict, Optional
from django.db import models
from django.db.models import Exists, OuterRef
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User
from traveldata.models import Cities, Sights, Foods, Shops, Sights_texts, Sights_imgs
from collectiondata.models import (
    UserSightCollection,
    UserFoodCollection,
    UserShopCollection,
)
from .models import Comment

from .decorator import ajax_check_login

# Create your views here.
"""-------------------------------------------------------------------------------------------"""


class HomepageView(ListView):
    template_name = "journing/index.html"
    context_object_name = "cities"
    model = Cities
    paginate_by = 12

    def get_queryset(self) -> QuerySet[Any]:
        # if no search is performed, return all cities
        q = self.request.GET.get("q")
        if not q:
            return super().get_queryset()

        # else return the related searches
        queryset = self.model.objects.filter(city__contains=q)
        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("q")
        return context


"""-------------------------------------------------------------------------------------------"""


# general template for sight,food and shop class to inherite from
class GeneralListView(ListView):
    template_name = "journing/detail.html"
    context_object_name = "items"
    paginate_by = 10

    # overide these variables
    collection_model = None
    collection_model_set = None
    current_page = None
    reverse_name = None

    def get_related_modelset(self):
        return self.request.GET.get("q")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["city"] = self.city
        context["current_page"] = self.current_page
        context["redirect_url"] = reverse_lazy(
            f"journing:{self.reverse_name}", args=[self.city.slug]
        )
        context["search"] = self.request.GET.get("q")
        return context

    def get_related_queryset(self):
        return self.collection_model.objects.filter(
            user=self.request.user, collection=OuterRef("pk")
        )

    # get the related query set and if user is logged in, retrieve their collections too
    def get_queryset(self) -> QuerySet[Any]:
        self.city = Cities.objects.get(slug=self.kwargs.get("slug"))

        queryset = self.get_related_modelset().prefetch_related(
            self.collection_model_set
        )

        if not self.request.user.is_anonymous:
            queryset = queryset.annotate(marked=Exists(self.get_related_queryset()))
        return queryset


class SightsListView(GeneralListView):
    collection_model = UserSightCollection
    collection_model_set = "usersightcollection_set"
    current_page = "sight"
    reverse_name = "sights_list"

    def get_related_modelset(self):
        q = super().get_related_modelset()
        if not q:
            return self.city.sights_set.all()
        return self.city.sights_set.filter(name__contains=q)


class FoodsListView(GeneralListView):
    collection_model = UserFoodCollection
    collection_model_set = "userfoodcollection_set"
    current_page = "food"
    reverse_name = "foods_list"

    def get_related_modelset(self):
        q = super().get_related_modelset()
        if not q:
            return self.city.foods_set.all()
        return self.city.foods_set.filter(name__contains=q)


class ShopsListView(GeneralListView):
    collection_model = UserShopCollection
    collection_model_set = "usershopcollection_set"
    current_page = "shop"
    reverse_name = "shops_list"

    def get_related_modelset(self):
        q = super().get_related_modelset()
        if not q:
            return self.city.shops_set.all()
        return self.city.shops_set.filter(name__contains=q)


"""-------------------------------------------------------------------------------------------"""


def sights_info_view(request, pk, slug):
    sight_obj = Sights.objects.filter(pk=pk)

    # retrieve the collection status in the detailed view
    if not request.user.is_anonymous:
        sight_obj = sight_obj.annotate(
            marked=Exists(
                UserSightCollection.objects.filter(
                    user=request.user, collection=OuterRef("pk")
                )
            )
        )
    sight_obj = sight_obj.first()

    sight_text = Sights_texts.objects.get(pk=pk)

    # code to modify and show the collection texts properly
    descs = str(sight_text.desc).split("->")
    titles = str(sight_text.title).split("->")
    info = []
    for i in range(len(titles)):
        descs[i] = descs[i].replace("\n", "</br>")
        temp = [titles[i], descs[i]]
        info.append(temp)

    sight_imgs = list(
        Sights_imgs.objects.select_related("sights")
        .filter(sights=pk)
        .values_list("img_local", flat=True)
    )

    context = {
        "sights_info": sight_text,
        "titles": titles,
        "descs": descs,
        "info": info,
        "imgs": sight_imgs,
        "slug": slug,
        "item": sight_obj,
    }

    return render(request, "journing/info.html", context)


class FoodsInfoView(DetailView):
    model = Foods
    template_name = "journing/unapplicable.html"

    def get_object(self, queryset=None):
        return super().get_object(queryset)


class ShopsInfoView(DetailView):
    model = Shops
    template_name = "journing/unapplicable.html"

    def get_object(self, queryset=None):
        return super().get_object(queryset)


"""-------------------------------------------------------------------------------------------"""


# display all the comments
class CommentsView(LoginRequiredMixin, ListView):
    template_name = "journing/comments.html"
    context_object_name = "comments"

    def get_queryset(self) -> QuerySet[Any]:
        return (
            Comment.objects.filter(sight=self.kwargs.get("pk"))
            .select_related("user__profile")
            .order_by("-created_on")
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["pk"] = self.kwargs.get("pk")
        context["slug"] = self.kwargs.get("slug")
        return context


class DeleteCommentView(View):
    @ajax_check_login
    def post(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=request.GET.get("id"))
        except:
            comment = None

        if not comment:
            return JsonResponse({"message": "no valid comment found!"})

        if not comment.user == self.user:
            return JsonResponse({"message": "unauthorized", "redirect_url": "/index/"})

        comment.delete()

        return JsonResponse({"message": "delete comment success!"})


class CreateCommentView(LoginRequiredMixin, CreateView):
    template_name = "journing/create_comment.html"
    model = Comment
    fields = ["rating", "comment"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.sight = Sights.objects.get(id=self.kwargs.get("pk"))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.object.get_absolute_url_sight()


class UpdateCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "journing/create_comment.html"
    fields = ["rating", "comment"]
    model = Comment

    def get_object(self) -> QuerySet[Any]:
        return self.model.objects.get(pk=self.kwargs.get("comment_pk"))

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.sight = Sights.objects.get(id=self.kwargs.get("pk"))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.object.get_absolute_url_sight()

    def test_func(self):
        return self.request.user == self.get_object().user
