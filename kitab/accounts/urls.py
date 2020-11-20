from django.contrib import admin
from django.urls import path
from accounts.views import MyProfileView, ProfileView

urlpatterns = [
    path('', MyProfileView.as_view(), name="my-profile"),
    path('<slug:slug>', ProfileView.as_view(),name="view-profile"),
]