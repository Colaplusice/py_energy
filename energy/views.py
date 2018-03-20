# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import MessageForm,UserForm
from .models import Message,Type
from django.contrib.auth import authenticate,logout,login
from django.shortcuts import render
import datetime
# Create your views here.
def index(request):
    all_messages=Message.objects.all()

    return render(request,'energy/index.html',{"all_messages":all_messages})


def detail(request):
    return  render(request,'energy/detail.html')

def submit_msg(request):
   if  not request.user.is_authenticated():
        return render(request,'energy/Login.html')
   else:
    if request.POST:
        message_form=MessageForm(request.POST or None,request.FILES or None)
        if message_form.is_valid():
            print("form is valid ")
            # message=Message(user=request.d)
            message=message_form.save(commit=False)
            message.img=request.FILES['img']
            message.title=message_form.cleaned_data['title']
            message.content=message_form.cleaned_data['content']
            message.type.name=message_form.cleaned_data['type']
            message.save()
            all_messages=Message.objects.filter(user=request.user)
            context_dict={}
            context_dict['errors']='添加成功'
            context_dict['all_messages']=all_messages
            return render(request,'energy/index.html',context_dict)
            # else:
            #     print(message_form)
            #     context_dict = {}
            #     all_types = Type.objects.all()
            #     form = MessageForm(request.POST or None, request.FILES or None)
            #     context_dict['all_types'] = all_types
            #     context_dict['error']="the form is not valid"
            #     return render(request, 'energy/submit_message.html',context_dict)
        else:
            print('表格错误')
            print(request.POST)
            # print(MessageForm.cleaned_data['title'])
            print(MessageForm.cleaned_data)
            # print(MessageForm.cleaned_data['type'])
            # print(request.FILES)
            error='the form is not valid'
            context_dict = {}
            all_types = Type.objects.all()
            form = MessageForm(request.POST or None, request.FILES or None)
            context_dict['form'] = form
            context_dict['all_types'] = all_types
            context_dict['error'] = error
            return render(request, 'energy/submit_message.html',context_dict)


    else:
        context_dict={}
        all_types = Type.objects.all()
        form=MessageForm(request.POST or None,request.FILES or None)
        context_dict['form']=form
        context_dict['all_types']=all_types
        return render(request, 'energy/submit_message.html',context_dict)


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
    context_dict={}
    messages=Message.objects.all()
    return render(request,'energy/forum.html',{'messages':messages})
