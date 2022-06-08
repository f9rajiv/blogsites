from django.shortcuts import render,get_object_or_404,redirect

from blog.forms import PostForm,CommentForm,ProfileForm
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
# Create your views here.

def user_profile(request, myid):
    post = Post.objects.filter(id=myid)
    return render(request, "user_profile.html", {'post':post})

def profile(request):
    return render(request, "profile.html")

def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method=="POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "edit_profile.html", {'alert':alert})
    else:
        form=ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {'form':form})



class AboutView(TemplateView):
    template_name='about.html'

class PostListView(ListView):

    model =Post   #connect to post model

    def get_queryset(self): #like sql query in django __lte is lessthanequal_to and '-' sign is about decesnding order print

        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):

    model=Post


#
class CreatePostView( LoginRequiredMixin,CreateView):

    login_url ='/login/'
    redirect_field_name ='blog/post_detail.html'

    form_class=PostForm
    model =Post
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView( LoginRequiredMixin,UpdateView):


    login_url ='/login/'
    redirect_field_name ='blog/post_detail.html'
    form_class=PostForm
    model =Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model =Post

    success_url =reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):

    login_url ='/login/'
    redirect_field_name ='blog/post_draft_list.html'
    model=Post

    def get_queryset(self): #like sql query in django __lte is lessthanequal_to and '-' sign is about decesnding order print
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


# below all required login so we use decorators
# @login_required(login_url = '/login')
# def post_new(request):
#     if request.method=="POST":
#         form = PostForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             blogpost = form.save(commit=False)
#             blogpost.author = request.user
#             blogpost.save()
#             obj = form.instance
#             # alert = True
#             return render(request, "post_detail.html",{'obj':obj})#, 'alert':alert})
#     else:
#         form=PostForm()
#     return render(request, "post_form.html", {'form':form})


@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method =='POST':
        form =CommentForm(request.POST)
        if form.is_valid():
            comment =form.save(commit=False)
            comment.post=post
            comment.writer=request.user


            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form=CommentForm()
    return render(request,'comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment =get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_ok=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post.pk)

def Register(request):
    if request.method=="POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')

        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')
    return render(request, "register.html")

def Login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, 'base.html')
    return render(request, "login.html")

def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')
