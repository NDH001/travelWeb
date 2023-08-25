from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "journing"
urlpatterns = [
    # -----------------------------------------------------------------------------------------------------#
    path("", views.HomepageView.as_view(), name="index"),
    # -----------------------------------------------------------------------------------------------------#
    path("sights/<slug:slug>/", views.SightsListView.as_view(), name="sights_list"),
    path("foods/<slug:slug>/", views.FoodsListView.as_view(), name="foods_list"),
    path("shops/<slug:slug>/", views.ShopsListView.as_view(), name="shops_list"),
    # -----------------------------------------------------------------------------------------------------#
    path(
        "sights/info/<str:pk>/<slug:slug>/", views.sights_info_view, name="sights_info"
    ),
    path(
        "foods/info/<str:pk>/<slug:slug>/",
        views.FoodsInfoView.as_view(),
        name="foods_info",
    ),
    path(
        "shops/info/<str:pk>/<slug:slug>/",
        views.ShopsInfoView.as_view(),
        name="shops_info",
    ),
    # -----------------------------------------------------------------------------------------------------#
    path(
        "sights/info/<str:pk>/<slug:slug>/comments/",
        views.CommentsView.as_view(),
        name="sights_comments",
    ),
    path(
        "sights/info/<str:pk>/<slug:slug>/comments/delete/",
        views.DeleteCommentView.as_view(),
        name="sights_delete",
    ),
    path(
        "sights/info/<str:pk>/<slug:slug>/comments/create/",
        views.CreateCommentView.as_view(),
        name="sights_create",
    ),
    path(
        "sights/info/<str:pk>/<slug:slug>/comments/update/<int:comment_pk>/",
        views.UpdateCommentView.as_view(),
        name="sights_update",
    ),
    path(
        "sights/comment/detail/",
        views.CommentDetailView.as_view(),
        name="sight_comment_detail",
    ),
    # -------------------------------------------------------------------------------#
    path("reset/notification/", views.ResetNotification.as_view(), name="reset_noti"),
    # -------------------------------------------------------------------------------#
    path("journal/", views.JournalView.as_view(), name="journal"),
    path("journal/new/", views.NewJournalView.as_view(), name="new_journal"),
    path("journal/save/", views.SaveJournal.as_view(), name="save_journal"),
    path("journal/edit/", views.EditJournal.as_view(), name="edit_journal"),
    path("journal/edit/<str:pk>/", views.EditJournal.as_view(), name="edit_journal"),
    path("journal/edit/get/<str:pk>/", views.GetJournal.as_view(), name="get_journal"),
]
