from typing import Any, Dict, Optional
from django.db import models
from django.db.models import Exists, OuterRef
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic import View, FormView
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
from .models import Comment, Notification, Record, Journal
from .forms import NewJournalForm

from .decorator import ajax_check_login

import json
import uuid

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
    paginate_by = 12

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


class CommentDetailView(DetailView):
    model = Comment
    template_name = "journing/detail_comment.html"
    context_object_name = "comment"

    def get_object(self, queryset=None):
        return Comment.objects.select_related("user", "sight", "user__profile").get(
            id=self.request.GET.get("q")
        )


# ---------------------------------------------------------------------------------------------------#


class ResetNotification(View):
    @ajax_check_login
    def post(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(user=self.user)
        notifications.delete()

        return JsonResponse({"message": "Notification reset success"})


# ---------------------------------------------------------------------------------------------------#


class JournalView(LoginRequiredMixin, FormView):
    template_name = "journing/journal.html"
    form_class = NewJournalForm
    success_url = reverse_lazy("journing:new_journal")

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {"form": self.form_class},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return self.form_invalid(form)

        return self.form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.prefetch_related(
            "usersightcollection_set",
            "userfoodcollection_set",
            "usershopcollection_set",
        ).get(pk=self.request.user.id)
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        self.request.session["destination"] = cleaned_data["where_to"].city
        self.request.session["start"] = cleaned_data["start_date"].isoformat()
        self.request.session["end"] = cleaned_data["start_date"].isoformat()

        return super().form_valid(form)


class NewJournalView(LoginRequiredMixin, View):
    template_name = "journing/new_journal.html"

    def get(self, request, *args, **kwargs):
        destination = request.session.get("destination")
        start = request.session.get("start")
        end = request.session.get("end")

        city = Cities.objects.get(pk=destination)

        sights = Sights.objects.filter(city=city)

        shops = Shops.objects.filter(city=city)

        foods = Foods.objects.filter(city=city)

        sight_collections = UserSightCollection.objects.filter(
            user=request.user, collection__in=sights
        ).select_related("user", "collection")

        food_collections = UserFoodCollection.objects.filter(
            user=request.user, collection__in=foods
        ).select_related("user", "collection")

        shop_collections = UserShopCollection.objects.filter(
            user=request.user, collection__in=shops
        ).select_related("user", "collection")

        hours = [
            "0000-0100",
            "0100-0200",
            "0200-0300",
            "0300-0400",
            "0400-0500",
            "0500-0600",
            "0600-0700",
            "0700-0800",
            "0800-0900",
            "0900-1000",
            "1000-1100",
            "1100-1200",
            "1200-1300",
            "1300-1400",
            "1400-1500",
            "1500-1600",
            "1600-1700",
            "1700-1800",
            "1800-1900",
            "1900-1000",
            "2000-2100",
            "2100-2200",
            "2200-2300",
            "2300-0000",
        ]

        return render(
            request,
            self.template_name,
            {
                "sight_collections": sight_collections,
                "food_collections": food_collections,
                "shop_collections": shop_collections,
                "hours": hours,
                "journal_id": uuid.uuid4(),
                "start": start,
                "end": end,
                "destination": destination,
            },
        )


class SaveJournal(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(data)

        try:
            journal = Journal.objects.get(pk=data["uuid"])
        except:
            journal = Journal.objects.create(
                pk=data["uuid"],
                user=self.request.user,
                start_date=data["start"],
                end_date=data["end"],
            )

        for record in data.items():
            hour = record[0]
            details = record[1]

            if hour == "uuid" or hour == "start" or hour == "end":
                continue

            if details["list_name"] == "sight_collections":
                ref = Sights.objects.get(pk=details["collection_id"])
            elif details["list_name"] == "food_collections":
                ref = Foods.objects.get(pk=details["collection_id"])
            else:
                ref = Shops.objects.get(pk=details["collection_id"])

            new_record = Record.objects.create(
                content_object=ref,
                hour=hour,
                remark=details["remark"],
                date=details["date"].strip(),
                journal=journal,
            )
            new_record.save()

        return JsonResponse({"message": "Journal saved!"})
