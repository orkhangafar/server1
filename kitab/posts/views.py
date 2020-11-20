from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormMixin, FormView, CreateView, UpdateView, DeleteView

from accounts.models import UserProfile
from posts.forms import CreateUserForm, CreatePostForm, UpdatePostForm
from posts.models import Post, Category


class SearchView(ListView):
    model = Post
    template_name = "posts/search.html"
    #paginate_by = 5
    context_object_name = "posts"
    #ordering = ['-created']


    def get_queryset(self):
        q = self.request.GET.get("q")
        if q:
            return Post.objects.filter(title__icontains=q).order_by('-created')
        return Post.objects.all()

class BaseView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        context['allCategories'] = Category.objects.all()
        context["profile"] = UserProfile.objects.get(user=self.request.user)
        return context

class IndexView(TemplateView):
    template_name = 'posts/index.html'

    #def get(self, request):
        #posts = Post.objects.all().order_by('-created')
        #args ={'posts' : posts}
        #return render(request, self.template_name,  args)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-created')
        context['allCategories'] = Category.objects.all()
        context['roman'] = Category.objects.get(slug='roman')
        return context

class PostDetail(DetailView):
    template_name = "posts/single.html"
    model = Post
    context_object_name = "single"

    def get_success_url(self):
        return reverse('single', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['allCategories'] = Category.objects.all()
        return context

#Category DEtailView
class CategoryDetail(DetailView):
    model = Category
    template_name = "posts/category.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail,self).get_context_data(**kwargs)
        context["allCategories"] = Category.objects.all()
        return context


#register Area
class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = CreateUserForm
    def form_valid(self, form):
        form.save()
        return redirect('login')

#createPost Area
@method_decorator(login_required(login_url='/login'),name="dispatch")
class CreatePostView(CreateView):
    template_name = 'posts/create_post.html'
    form_class = CreatePostForm

    def get_success_url(self):
        return reverse("single",kwargs={"slug":self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePostView, self).form_valid(form)

#Updateview
@method_decorator(login_required(login_url='/login'),name="dispatch")
class UpdatePostView(UpdateView):
    model = Post
    template_name = 'posts/update_post.html'
    form_class = UpdatePostForm

    def get_success_url(self):
        return reverse("single",kwargs={"slug":self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UpdatePostView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(UpdatePostView, self).get(request, *args, **kwargs)

#DeleteView
@method_decorator(login_required(login_url='/login'),name="dispatch")
class PostdeleteView(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'posts/delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect('/')
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(PostdeleteView,self).get(request,*args,**kwargs)




