from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models import Count
from rest_framework import generics, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from datetime import timedelta

from .models import *
from .serializers import *
from .permissions import IsOwnerOrReadOnly
from .forms import *

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsOwnerOrReadOnly]

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        car_id = self.kwargs.get('id')
        try:
            Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            raise NotFound(detail="No Car matches the given query.")
        return Comment.objects.filter(car=car_id)
    
    def perform_create(self, serializer):
        car_id = self.kwargs.get('id')
        try:
            Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            raise NotFound(detail="No Car matches the given query.")
        serializer.save(car=car_id)

def LoginUser(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            
            if user != None:
                login(request, user)
                return redirect('index')
    
    form = LoginForm()
    return render(request, 'cars/login.html', {'form': form})
    
def LogoutUser(request):
    logout(request)
    request.user = None
    return redirect('index')

def RegisterUser(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = True
            user.save()

            login(request, user)

            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'cars/registration.html', {'form': form})

def index(request):
    users = User.objects.filter(cars__created_at__gte=(now() - timedelta(days=365))).annotate(car_count=Count('cars')).order_by('-car_count')[:10]
    cars = Car.objects.all().order_by('-created_at')[:10]

    return render(request, 'cars/index.html', {'cars': cars, 'users': users})

def cars(request):
    cars = Car.objects.all().order_by('created_at')
    count = len(cars)
    return render(request, 'cars/cars.html', {'cars': cars, 'count': count})

def car(request, id):
    car = get_object_or_404(Car, id=id)
    comments = Comment.objects.filter(car=id).order_by('created_at')

    if request.user.is_authenticated:
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = User.objects.filter(id=request.user.id).first()
                comment.car = Car.objects.filter(id=id).first()
                comment.save()
                return redirect('car_detail', id)
        
        form = CommentForm()
        return render(request, 'cars/car.html', {'car': car, 'comments': comments, 'form': form})

    return render(request, 'cars/car.html', {'car': car, 'comments': comments})

def user(request, username):
    userpage = get_object_or_404(User, username=username)

    cars = Car.objects.filter(owner=userpage.id).order_by('created_at')
    count = len(cars)

    return render(request, 'cars/user.html', {'userpage': userpage, 'cars': cars, 'count': count})

@login_required(login_url="/login")
def car_create(request):
    if request.method == "POST":
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = User.objects.filter(id=request.user.id).first()
            car.save()
            return redirect('user_page', request.user.username)
    else:
        form = CarForm()
    return render(request, 'cars/edit.html', {'form': form})

@login_required(login_url="/login")
def car_edit(request, id):
    car = get_object_or_404(Car, id=id, owner=request.user.id)
    if request.method == "POST":
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            car = form.save()
            return redirect('user_page', request.user.username)
    else:
        form = CarForm(instance=car)
    return render(request, 'cars/edit.html', {'form': form})

@login_required(login_url="/login")
def car_delete(request, id):
    car = get_object_or_404(Car, id=id, owner=request.user.id)
    car.delete()
    return redirect('user_page', request.user.username)
