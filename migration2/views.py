from django.shortcuts import render
from django.shortcuts import redirect
from mylogin import settings
from . import models
from . import forms

import hashlib
import datetime
# Create your views here.

def index(request):
    pass
    return render(request, 'migration2/index.html')

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = user.name
    models.ConfirmString.objects.create(code=code, user=user)
    return code

def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '來自www.liujiangblog.com的註冊確認郵件'

    text_content = '''感謝註冊www.liujiangblog.com\
                    如果你看到這條消息，說明你的郵箱服務器不提供HTML鏈接功能，請聯繫管理員！'''

    html_content = '''
                    <p>感謝註冊<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，\
                    這裡是劉江的博客和教程站點</p>
                    <p>請點擊站點鏈接完成註冊確認</p>
                    <p>此鏈接有效期為{}天</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def login(request):
    if request.session.get('is_login', None):  #不給重複登入
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '所有空格都須填寫'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '帳號不存在'
                return render(request, 'migration2/login.html', locals())

            if not user.has_confirmed:
                message = '註冊碼尚未確認'
                return render(request, 'migration2/login.html', locals())

            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密碼錯誤'
                return render(request, 'migration2/login.html', locals())
        else:
            return render(request, 'migration2/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'migration2/login.html',locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')               #若是已登入，點註冊就會導回首頁
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = '請檢查填寫內容'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']        #拿取用戶填寫的資料，存到各自變數
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:                         #擋住情況：兩次密碼輸入不同、用戶名已註冊、信箱已註冊
                message = "兩次輸入的密碼須相同"
                return render(request, 'migration2/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message= "用戶名已註冊，請重新選擇"
                    return render(request, 'migration2/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '該信箱已註冊過'
                    return render(request, 'migration2/register.html', locals())

            new_user = models.User.objects.create()
            new_user.name = username
            new_user.password = hash_code(password1)
            new_user.email = email
            new_user.sex = sex
            new_user.save()
            return redirect('/login/')

            code = make_confirm_string(new_user)
            send_email(email, code)

            message = '請前往信箱確認'
            return render(request, 'migration2/confirm.html', locals())
        else:
            return render(request, 'migration2/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'migration2/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/login/')  #沒有logout的頁面，導回到index畫面


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        comfirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '無效的請求'
        return render(request, 'migration2/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()

    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '確認碼已過期，請重新註冊'
        return render(request, 'migration2/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感謝確認，請登入！'
        return render(request, 'migration2/confirm.html', locals())