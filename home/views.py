from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import BlogForm
from .models import Blog, Diskus
from django.contrib.auth.decorators import login_required

def home(request):
    writer = Blog.objects.all()
    comments = Diskus.objects.all().order_by('-created')
    return render(request, 'home/home.html', {'writer':writer, 'comments':comments})

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'home/signupuser.html', {'form':UserCreationForm()})
    else:
        if len(request.POST['password1']) == 8:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('home')
                except IntegrityError:
                    return render(request, 'home/signupuser.html', {'form':UserCreationForm(), 'error':'Такой пользователь уже есть!'})


            else:
                return render(request, 'home/signupuser.html', {'form':UserCreationForm(), 'error':'Пароли не совпадают!'})
        else:
                return render(request, 'home/signupuser.html', {'form':UserCreationForm(), 'error':'Минимальная дляна пароля 8 символов!'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'home/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'home/loginuser.html', {'form':AuthenticationForm(), 'error':'Пароль или логин неверны'})
        else:
            login(request, user)
            return redirect('home')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def discussion(request):
    comments = Diskus.objects.all().order_by('-created')
    if request.method == 'GET':
        return render(request, 'home/comment.html', {'form':BlogForm(), 'comments':comments})
    else:
        try:
            form = BlogForm(request.POST)
            newblog = form.save(commit=False)
            newblog.user = request.user
            newblog.save()
            return redirect('discussion')
        except ValueError:
            return render(request, 'home/comment.html', {'form':BlogForm(), 'error':'Введены неверные параметры'})
    


# def createblog(request):
#     if request.method == 'GET':
#         return render(request, 'home/comment.html', {'form':BlogForm()})
#     else:
#         try:
#             form = BlogForm(request.POST)
#             newblog = form.save(commit=False)
#             newblog.user = request.user
#             newblog.save()
#             return redirect('discussion')
#         except ValueError:
#             return render(request, 'home/comment.html', {'form':BlogForm(), 'error':'Введены неверные параметры'})

@login_required
def currentblog(request):
    myposts = Diskus.objects.filter(user=request.user).order_by('-created')
    return render(request, 'home/currentblog.html', {'myposts':myposts})

@login_required
def viewpost(request, post_pk):
    post = get_object_or_404(Diskus, pk=post_pk, user=request.user)
    if request.method == 'GET':
        form = BlogForm(instance=post)
        return render(request, 'home/viewpost.html', {'post':post, 'form':form})
    else:
        try:
            form = BlogForm(request.POST, instance=post)
            form.save()
            return redirect('discussion')
        except ValueError:
            return render(request, 'home/viewpost.html', {'post':post, 'form':form, 'error':'Введены неверные параметры'})


@login_required
def deletepost(request, post_pk):
    post = get_object_or_404(Diskus, pk=post_pk, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('discussion')