from __future__ import unicode_literals

from io import BytesIO
from typing import Dict, Union

import markdown
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from utils import image_2
from .forms import MessageForm, UserForm
from .models import *


# Create your views here.
def index(request):
    all_messages = Message.objects.all()
    types = Type.objects.all()
    context_dict = {"all_types": types, "all_messages": all_messages}
    return render(request, "energy/index.html", context_dict)


def detail(request, message_id):
    msg = Message.objects.get(id=int(message_id))
    if msg:
        msg.views += 1
    msg.save()
    comment = Commit.objects.filter(message=msg)
    context_dict = {"message": msg, "comment": comment}
    return render(request, "energy/detail.html", context_dict)


def submit_msg(request):
    if not request.user.is_authenticated:
        return render(request, "energy/login.html")
    else:
        if request.POST:
            message_form = MessageForm(request.POST or None, request.FILES or None)
            if message_form.is_valid():
                print("form is valid")
                # message=Message(user=request.d)
                message = message_form.save(commit=False)
                if not request.FILES:
                    message.img = None

                message.title = message_form.cleaned_data["title"]
                message.content = message_form.cleaned_data["content"]
                message.type.name = message_form.cleaned_data["type"]
                message.save()
                all_messages = Message.objects.filter(user=request.user)
                context_dict = {"errors": "添加成功", "all_messages": all_messages}
                return render(request, "energy/index.html", context_dict)
            else:
                error = "the form is not valid"
                context_dict = {}
                all_types = Type.objects.all()
                form = MessageForm(request.POST or None, request.FILES or None)
                context_dict["form"] = form
                context_dict["all_types"] = all_types
                context_dict["error"] = error
                return render(request, "energy/submit_message.html", context_dict)

        else:
            context_dict = {}
            all_types = Type.objects.all()
            form = MessageForm(request.POST or None, request.FILES or None)
            context_dict["form"] = form
            context_dict["all_types"] = all_types
            return render(request, "energy/submit_message.html", context_dict)


def articles(request):
    page_num = request.GET.get('page_id')
    page_num = int(page_num)
    if page_num is None or page_num < 0:
        page_num = 1
    pages = Article.objects.all()
    begin = 5 * (page_num - 1)
    end = 5 * page_num
    article_list = Article.objects.order_by("-views")[begin:end]
    # 得到cat和page 和 article的信息
    context_dict = {"articles": article_list, "page": pages}
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
    response = render(request, "energy/article.html", context_dict)
    return response


def blog(request, blog_id):
    contents = Article.objects.get(pk=blog_id)
    # 支持markdown显示
    contents.content = markdown.markdown(
        contents.content,
        extentions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            "markdown.extensions.toc",
        ],
    )

    context_dict = {
        "content": contents.content,
        "title": contents.title,
        "date": contents.pub_date,
        "author": contents.user,
    }
    return render(request, "energy/article_detail.html", context_dict)


def login(request):
    # ver_code
    context_dict: Dict[
        str, Union[UserForm, str, QuerySet[Message], QuerySet[Type]]
    ] = {}
    user_form = UserForm()
    context_dict["form"] = user_form
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        ver_code = request.POST["ver_code"]
        true_code = request.session.get("ver_code")
        if true_code == ver_code:
            pass
        else:
            context_dict["error"] = "验证码错误"
            return render(request, "energy/login.html", context_dict)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages = Message.objects.all()
            all_types = Type.objects.all()
            context_dict["all_messages"] = messages
            context_dict["all_types"] = all_types
            return render(request, "energy/index.html", context_dict)
        else:
            return render(request, "energy/login.html", {"error": "an error happened"})
    else:
        return render(request, "energy/login.html", context_dict)


def log_out(request):
    log_out(request)
    form = UserForm(request.POST or None)
    context = {"form": form}
    return render(request, "energy/login.html", context)


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            print(request.POST)
            print("收到请求")
            context_dict = {"error": "s", "form": form}
            return render(request, "energy/register.html", context_dict)
        else:
            error = "register form is not valid"
            print(request)
            context_dict = {"error": error, "form": form}
            return render(request, "energy/register.html", context_dict)
    else:
        error = "this is get request"
        context_dict = {}
        form = UserForm()
        context_dict["form"] = form
        context_dict["error"] = error
        return render(request, "energy/register.html", context_dict)


def sendmail(request):
    send_mail("发送", "message", "fjl2401@163.com", fail_silently=False)
    return HttpResponse("success")


def forum(request):
    context_dict = {}
    messages = Message.objects.all()
    comment = Commit.objects.filter(message__in=messages)
    context_dict["comment"] = comment
    context_dict["messages"] = messages
    return render(request, "energy/forum.html", context_dict)


def yz_home(request):
    if request.method == "GET":
        return render(request, "energy/yz_home.html")
    else:
        return HttpResponse("ok")


def verify(request):
    f = BytesIO()
    img, code = image_2.create_code()
    request.session["ver_code"] = code
    img.save(f, "PNG")
    return HttpResponse(f.getvalue())


@csrf_exempt
def test_1(request):
    print(request.is_ajax())

    return render(request, "energy/test_1.html")
