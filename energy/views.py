# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import MessageForm,UserForm
from .models import *
import string
import random
from utils import Random_image
import website.settings as settings
from django.contrib.auth import authenticate,logout,login
from django.shortcuts import render,HttpResponse
from django.core.mail import send_mail
from utils.email_send import Token
import datetime
# Create your views here.
def index(request):
    all_messages=Message.objects.all()
    types=Type.objects.all()
    context_dict={}
    context_dict['all_types']=types
    context_dict['all_messages']=all_messages
    return render(request,'energy/index.html',context_dict)


def detail(request,Message_id):
    msg=Message.objects.get(id=int(Message_id))
    if msg: msg.views+=1
    msg.save()
    comment=Commit.objects.get_or_create(message=msg)
    context_dict={}
    context_dict['message']=msg
    context_dict['comment']=comment

    return  render(request,'energy/detail.html',context_dict)

def submit_msg(request):
   if  not request.user.is_authenticated():
        return render(request,'energy/Login.html')
   else:
    if request.POST:
        message_form=MessageForm(request.POST or None,request.FILES or None)
        if message_form.is_valid():
            print("form is valid")
            # message=Message(user=request.d)
            message=message_form.save(commit=False)
            if not request.FILES:
                message.img = None

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

def Articles(request):
    if request.GET.get('page_id') is None:
        pagenum = 1
    else:
        print(request.GET.get('page_id'))
        pagenum = request.GET.get('page_id')
        pagenum = int(pagenum)
    context_dict = {}
    if pagenum > 0:
        begin = 5 * (pagenum - 1)
        end = 5 * pagenum
        # 得到所有的文章 来计算需要几页
        all_article = Article.objects.count()
        page = all_article / 5
        if all_article % 5 != 0:
            page += 1
        pages = []
        for i in range(1, page + 1):
            pages.append(i)
        article_list = Article.objects.order_by('-views')[begin:end]
    else:
        article_list = Article.objects.order_by('-views')[:3]
    # 得到cat和page 和 article的信息
    context_dict = {'articles': article_list, 'page': pages}
    # 得到session值
    # visits = request.session.get('visit')
    # if not visits:
    #     visits = 2
    # reset_last_visit_time = False
    # # 是否有最后一次登录
    # last_visit = request.session.get('last_visit')
    # if last_visit:
    #     last_visit_time = datetime.strptime(last_visit[:-7], '%Y-%m-%d %H:%M:%S')
    #     if (datetime.now() - last_visit_time).seconds > 0:
    #         visits = visits + 1
    #         reset_last_visit_time = True
    # else:
    #     reset_last_visit_time = True
    # if reset_last_visit_time:
    #     request.session['last_visit'] = str(datetime.now())
    #     request.session['visit'] = visits
    # context_dict['visits'] = visits
    response = render(request, 'energy/article.html', context_dict)
    return response

def Blog(request,blog_id):
        contents = Article.objects.get(pk=blog_id)
        return render(request, 'energy/article_detail.html', {'article':contents})

def Login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages=Message.objects.all()
            all_types=Type.objects.all()
            contenxt_dict={}
            contenxt_dict['all_messages']=messages
            contenxt_dict['all_types']=all_types
            return render(request,'energy/index.html',contenxt_dict)
        else:
            return  render(request,'energy/Login.html',{'error':'an error happened'})
    else:
        #ver_code
        ver_code_path=settings.VERIFICATION_CODE_DIR
        today_str = datetime.date.today().strftime("%Y%m%d")
        ver_code_img_path="%s%s"%(ver_code_path,today_str)
        random_filename = "".join(random.sample(string.ascii_lowercase, 4))
        random_code = Random_image.verify_code.gene_code(ver_code_img_path, random_filename)
        # cache.set(random_filename, random_code, 30)
        user_form=UserForm(request.POST or None)

        return render(request,'energy/Login.html',{'form':user_form})


def Logout(request):
    logout(request)
    form=UserForm(request.POST or None)
    context={'form':form }
    return render(request,'energy/Login.html',context)


def Register(request):
    if request.method=='POST':
        form=UserForm(request.POST)

        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']
            user=form.save()
            token=Token.generate_validate_token(username)
            # message = "\n".join([u'{0},欢迎加入我的博客'.format(username), u'请访问该链接，完成用户验证:',
            #                      '/'.join([Dja.DOMAIN, 'activate', token])])
            message='欢迎访问我的博客'
            user.send
            #return
            # new_user=User(username=username,password=password,email=email)
            # new_user.is_active=False
            # new_user.save()
            if user.is_active:
                message = Message.objects.filter(user=request.user)
                return render(request, 'energy/index.html', {'messages': message})
        else:
            error='register form is not valid'
            context_dict={}
            context_dict['error']=error
            context_dict['form']=form
            return render(request,'energy/register.html',context_dict)
    else:
        print(request.method)
        error='this is get request'
        context_dict={}
        form=UserForm()
        context_dict['form']=form
        context_dict['error']=error

        return render(request,'energy/register.html',context_dict)

def sendmail(request):
    send_mail('发送','message','fjl2401@163.com',fail_silently=False)
    return   HttpResponse('success')

def Forum(request):
    context_dict={}
    messages=Message.objects.all()
    comment=Commit.objects.get_or_create(message=messages)
    context_dict['comment']=comment
    context_dict['messages']=messages
    return render(request,'energy/forum.html',context_dict)

