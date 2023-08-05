from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import Chatroomform 
from .models import Chatroom,Topic,Messages

# Create your views here.
def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect("homepage")
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user= User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist!")
        
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('homepage')
        else:
            messages.error(request,"username or password is incorrect!")

    context={'page':page}
    return render(request,"basic/login_form.html/",context)

def logoutuser(request):
    logout(request)
    return redirect('homepage')

def registeruser(request):
    form=UserCreationForm()
    if request.method =='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('homepage')
    return render(request,"basic/login_form.html/",{'form':form})

def homepage(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    recent_mgs=Messages.objects.filter(Q(room__topic__name__icontains=q)
                                        # |Q(user__name__icontains=q)
                                       ).order_by("-created")
    rooms= Chatroom.objects.filter(Q(topic__name__icontains=q)
                                   | Q(name__icontains=q)
                                #    | Q(host=q)
                                     | Q(description__icontains=q) )
    topic = Topic.objects.all()
    roomscount = rooms.count()
    context = {"rooms" :rooms,'topic':topic,'count':roomscount,'msgs':recent_mgs}
    return render(request, "basic/home.html", context)
def userprofile(request,pk):
    user=User.objects.get(id=pk)
    recent_mgs=Messages.objects.filter(user__id=pk)
    rooms=Chatroom.objects.filter(host__id=pk)
    rooms1=Chatroom.objects.filter(members__id=pk)
    topics=Topic.objects.all()
    context={'user':user ,'msgs':recent_mgs,'rooms':rooms,'rooms1':rooms1,"topic":topics,"count":Chatroom.objects.all().count()}
    return render(request,"basic/userprofile.html",context)
def chatroom(request,pk):
    room=Chatroom.objects.get(id=pk)
    room_messages=room.messages_set.all().order_by("-created")
    members=room.members.all()
    if request.method=="POST":
        message=Messages.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body")
        )
        room.members.add(request.user)
        return redirect("chatroom",pk=room.id)
    context={'room': room,'room_messages':room_messages,'members':members}
    return render(request, "basic/chatroom.html",context)
@login_required(login_url="loginpage")
def chatroomform(request):
    form=Chatroomform()
    topics=Topic.objects.all()
    if request.method=="POST":
            topic_name=request.POST.get('topic')
            topic, created=Topic.objects.get_or_create(name=topic_name)
            Chatroom.objects.create(
                host=request.user,
                topic=topic,
                name=request.POST.get('name'),
                description=request.POST.get('description]'),

            )

        # form=Chatroomform(request.POST)
        # if form.is_valid():
        #     room= form.save()
        #     room.host=request.user
        #     room.save()
            return redirect('homepage')
    context = {'form' : form ,'topics':topics}
    return render(request,'basic/chatroom_form.html',context)
@login_required(login_url="loginpage")
def editchatroom(request,pk):
    room=Chatroom.objects.get(id=pk)
    form=Chatroomform(instance=room)
    topics=Topic.objects.all()
    if request.user!=room.host:
        return HttpResponse("Only owners can edit thier rooms")
    if request.method=="POST":
        topic_name=request.POST.get('topic')
        topic, created=Topic.objects.get_or_create(name=topic_name)
        room.topic=topic
        room.name=request.POST.get('name')
        room.description=request.POST.get('description]')
        room.save()
        return redirect('homepage')
    context={'form':form,'topics':topics,'room':room}
    return render(request,"basic/chatroom_form.html",context)
@login_required(login_url="loginpage")  
def deletechatroom(request,pk):
    room=Chatroom.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse("Only owners can delete thier rooms")
    if request.method=='POST':
        room.delete()
        return redirect('homepage')
    return render(request,'basic/delete.html',{'obj': room})
@login_required(login_url="loginpage")  
def deletemessage(request,pk):
    message=Messages.objects.get(id=pk)
    if request.user!=message.user:
        return HttpResponse("Only owners can delete thier messages")
    if request.method=='POST':
        message.delete()
        return redirect("chatroom",pk=message.room.id)
    return render(request,'basic/delete.html',{'obj': message})
@login_required(login_url='loginpage')
def updateuser(request):
    context={
    }
    return render(request, 'basic/updateuser.html',context)