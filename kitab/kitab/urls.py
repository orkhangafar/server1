"""kitab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as authViews

from posts.views import RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('profile/', include('accounts.urls')),
    path('login/', authViews.LoginView.as_view(),name="login"),
    path('logout/', authViews.LogoutView.as_view(),name="logout"),
    path('register/', RegisterView.as_view() ,name="register"),
    path('password/change/', authViews.PasswordChangeView.as_view(template_name='registration/password-change.html'),name="password-change"),
    path('password/change/done', authViews.PasswordChangeDoneView.as_view(template_name='registration/password-change-done.html'),name="password_change_done"),

    path('reset_password/',authViews.PasswordResetView.as_view(template_name='registration/password_reset.html'),name="reset_password"),
    path('reset_password_sent',authViews.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',authViews.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/',authViews.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
