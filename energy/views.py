# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import MessageForm,UserForm
from .models import Message
from django.contrib.auth import authenticate,logout,login
from django.shortcuts import render
# Create your views here.
def index(request):
    all_messages=Message.objects.all()

    return render(request,'energy/index.html',{"all_messages":all_messages})


def submit_msg(request):
    if request.user.is_authenticated():
        if request.POST:
            print(request.POST)
            print(request.POST['content'])
            print(type(request.FILES))
            message_form=MessageForm(request.POST or None ,request.FILES or None)
            # print(message_form)
            # print(message_form.cleaned_data['title'])
            # print(message_form.cleaned_data['content'])
            # print(request.FILES['img'])
            if message_form.is_valid():
                message=message_form.save(commit=False)
                message.img=request.FILES['img']
                message.title=message_form.cleaned_data['title']
                message.content=message_form.cleaned_data['content']
                print('yes')
                message.save()
                all_messages=Message.objects.filter(user=request.user)

                return render(request,'energy/index.html',{"all_messages":all_messages})
            else:
                print(message_form)

                return render(request, 'energy/submit_message.html',{"error":"the form is not vaild"})

        else:
            form=MessageForm(request.POST or None,request.FILES or None)

    else: return render(request,'energy/Login.html')
    return render(request,'energy/submit_message.html',{"form":form})


def Login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages=Message.objects.filter(user=request.user)
            return render(request,'energy/index.html',{'messages':messages})
        else:
            return  render(request,'energy/Login.html',{'error':'an error happened'})
    else:
        user_form=UserForm(request.POST or None)

        return render(request,'energy/Login.html',{'form':user_form})


def Logout(request):
    logout(request)
    form=UserForm(request.POST or None)
    context={'form':form }
    return render(request,'energy/Login.html',context)


def Register(request):
    if request.method=='POST':
        form=UserForm(request.POST or None)
        if form.is_valid():
            new_user=form.save(commit=False)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            new_user.set_password(password)
            new_user.save()
            #return
            new_user=authenticate(username=username,password=password)
            if new_user.is_active():
                message=Message.objects.filter(user=request.user)
                return render(request,'energy/index.html',{'messages':message})
    return render(request,'energy/Register.html')

def Forum(request):
    return render(request,'energy/forum.html')