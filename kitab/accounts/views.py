from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView

from accounts.models import UserProfile


@method_decorator(login_required(login_url="/login"),name="dispatch")
class MyProfileView(TemplateView):
    template_name = "profile/user.html"


    def get_context_data(self, **kwargs):
        context = super(MyProfileView,self).get_context_data(**kwargs)
        context["profile"] = UserProfile.objects.get(user=self.request.user)
        return context

@method_decorator(login_required(login_url="/login"),name="dispatch")
class ProfileView(DetailView):
    model = UserProfile
    template_name = "profile/view.html"
    context_object_name = "profile"

    #def get_context_data(self, **kwargs):
        #context = super(ProfileView, self).get_context_data(**kwargs)
        #myprofile = self.request.user.profile.get()
        #return context
