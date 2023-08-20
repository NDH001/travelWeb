from typing import Any, Callable, Dict, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import F, Exists
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
import json

from .forms import UserLoginForm, UserRegForm, UserUpdateForm, ProfileUpdateForm
from .models import Connection
from journing.models import Notification
from journing.decorator import ajax_check_login

from django.urls import reverse_lazy


# Create your views here.


class UserLoginView(FormView):
    template_name = "userdata/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("journing:index")

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = self.form_class()
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return self.form_valid(form)

        messages.error(request, "Username and password does not match")

        return self.form_invalid(form)


class UserRegisterView(FormView):
    template_name = "userdata/register.html"
    form_class = UserRegForm

    success_url = reverse_lazy("journing:index")

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return self.form_invalid(form)

        return self.form_valid(form)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


"""----------------------------------------------------------------------------"""


# profile views
class ProfileView(UserPassesTestMixin, DetailView):
    model = User
    template_name = "userdata/profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def test_func(self):
        return self.request.user == get_object_or_404(
            self.model, username=self.kwargs.get("username")
        )

    def get_object(self, queryset=None):
        return self.model.objects.prefetch_related(
            "comment_set", "comment_set__sight"
        ).get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["following"] = Connection.objects.filter(
            follower=self.request.user
        ).count()
        context["followers"] = Connection.objects.filter(user=self.request.user).count()
        return context


def user_logout(request):
    logout(request)
    return redirect("journing:index")


class EditProfileView(FormView):
    template_name = "userdata/edit_profile.html"
    user_form_class = UserUpdateForm
    profile_form_class = ProfileUpdateForm

    success_url = reverse_lazy("journing:index")

    def get(self, request, *args, **kwargs):
        u_form = self.user_form_class(instance=request.user)
        p_form = self.profile_form_class(instance=request.user.profile)
        return render(
            request, self.template_name, context={"u_form": u_form, "p_form": p_form}
        )

    def post(self, request, *args, **kwargs):
        u_form = self.user_form_class(request.POST, instance=request.user)
        p_form = self.profile_form_class(
            request.POST, request.FILES, instance=request.user.profile
        )

        if not (u_form.is_valid() and p_form.is_valid()):
            return self.form_invalid(u_form, p_form)

        return self.form_valid(u_form, p_form)

    def form_valid(self, u_form, p_form):
        u_form.save()
        p_form.save()
        return super().form_valid(u_form)

    def form_invalid(self, u_form, p_form):
        return render(
            self.request,
            self.template_name,
            {
                "u_form": u_form,
                "p_form": p_form,
                "u_errors": u_form.errors.values(),
                "p_errors": p_form.errors.values(),
            },
        )


"""----------------------------------------------------------------------------"""


# connections
class PeekView(DetailView):
    template_name = "userdata/peek.html"
    context_object_name = "target_user"

    def get_object(self, queryset=None):
        self.target_user = (
            User.objects.select_related("profile")
            .prefetch_related("comment_set", "comment_set__sight")
            .get(pk=self.kwargs.get("pk"))
        )
        return self.target_user

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            is_following = Connection.objects.get(
                user=self.target_user, follower=self.request.user
            )
        except:
            is_following = None

        context["is_following"] = is_following
        context["followers"] = Connection.objects.filter(user=self.request.user).count()
        context["following"] = Connection.objects.filter(
            follower=self.request.user
        ).count()

        return context


class Connect(View):
    @ajax_check_login
    def post(self, request, *args, **kwargs):
        self.target_user = User.objects.get(username=request.POST.get("target_user"))
        try:
            self.connection = Connection.objects.get(
                user=self.target_user, follower=self.user
            )
        except:
            self.connection = None


class Follow(Connect):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if self.connection:
            return JsonResponse({"message": "Already Followed!"})

        connection = Connection.objects.create(
            user=self.target_user, follower=self.user
        )
        connection.save()

        notification = Notification.objects.create(
            user=self.target_user, message=f"{self.user} followed you !"
        )

        notification.save()

        return JsonResponse({"message": "Followed!"})


class Unfollow(Connect):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if not self.connection:
            return JsonResponse({"message": "Already unfollowed!"})

        self.connection.delete()

        return JsonResponse({"message": "Unfollowed!"})


"""-----------------------------------------------------------------------"""
# connection view


class FollowersView(ListView):
    template_name = "userdata/followers.html"
    context_object_name = "connections"
    paginate_by = 13

    def get_queryset(self) -> QuerySet[Any]:
        followers = Connection.objects.filter(
            user_id=self.kwargs.get("pk")
        ).select_related("user", "follower__profile")

        return followers

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        following = list(
            Connection.objects.filter(follower=self.kwargs.get("pk")).values_list(
                "user", flat=True
            )
        )
        context["following"] = following
        return context


class FollowingView(ListView):
    template_name = "userdata/following.html"
    context_object_name = "connections"
    paginate_by = 13

    def get_queryset(self) -> QuerySet[Any]:
        return Connection.objects.filter(follower=self.kwargs.get("pk")).select_related(
            "user", "follower", "user__profile"
        )
