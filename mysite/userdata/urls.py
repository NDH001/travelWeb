from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name ='userdata'
urlpatterns = [
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout',views.user_logout,name='logout'),
    path('register/',views.UserRegisterView.as_view(),name='register'),
    path('profile/<slug:username>/',views.ProfileView.as_view(),name='profile'),
    path('profile/<slug:username>/edit/',views.EditProfileView.as_view(),name='edit')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
