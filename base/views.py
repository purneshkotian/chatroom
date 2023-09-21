from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {'id': 1, 'name': 'room 1 in the house'},
#     {'id': 2, 'name': 'room 2 in the house'},
#     {'id': 3, 'name': 'room 3 in the house'}
# ]
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password does not exist")

    return render(request, 'login_register.html')

def logoutPage(request):
    logout(request)
    return render(request, 'home.html')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else " "
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms':rooms, 'topics':topics, 'room_count': room_count}
    return render(request, 'home.html', context)

def room(request, val):
    room = Room.objects.get(id = val)
    context = {'room': room}
    return render(request, 'room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'delete.html', {'obj': room})
