from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ToDoForm
from .models import Tasks
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error': 'User is already Taken, please choose another user.'})
        else:
            return render(request, 'todo/signup.html', {'form': UserCreationForm(), 'error': 'Password did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, password=request.POST['password'], username=request.POST['username'])
        if user is not None:
            login(request, user)
            return redirect('currenttodos')
        else:
            return render(request, 'todo/login.html', {'form': AuthenticationForm(), 'error': 'username and password is invalid'})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/create.html', {'form': ToDoForm()})
    else:
        try:
            form = ToDoForm(request.POST)
            newTodo = form.save(commit=False)
            newTodo.user = request.user
            newTodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/create.html', {'form': ToDoForm(), 'error': 'Passing Bad Data. Please Try again'})


@login_required
def currenttodos(request):
    todos = Tasks.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'todo/current.html', {'todos': todos})


@login_required
def completed(request):
    todos = Tasks.objects.filter(
        user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request, 'todo/completed.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Tasks, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = ToDoForm(instance=todo)
        return render(request, 'todo/todo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = ToDoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/todo.html', {'form': form})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Tasks, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.dateCompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Tasks, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
