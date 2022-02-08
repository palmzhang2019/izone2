import json
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from izone import settings
from .forms import ProfileForm
from django.contrib import messages
from urllib import parse, request as lib_request
from django.http import HttpResponseRedirect
from .models import Ouser
from django.urls import reverse


# Create your views here.

@login_required
def profile_view(request):
    return render(request, 'oauth/profile.html')


@login_required
def change_profile_view(request):
    if request.method == 'POST':
        # 上传文件需要使用request.FILES
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # 添加一条信息,表单验证成功就重定向到个人信息页面
            messages.add_message(request, messages.SUCCESS, '个人信息更新成功！')
            return redirect('oauth:profile')
    else:
        # 不是POST请求就返回空表单
        form = ProfileForm(instance=request.user)
    return render(request, 'oauth/change_profile.html', context={'form': form})


# 这里不是很明白
def _get_refer_url(request):
    refer_url = request.META.get('HTTP_REFER',
                                 '/index(自己的首页)')
    host = request.META['HTTP_HOST']
    if refer_url.startswith('http') and host not in refer_url:
        refer_url = '/index'
    return refer_url


# 第一步: 请求github第三方登录
def githhub_login(request):
    data = {
        'client_id': settings.GITHUB_CLIENTID,
        'client_secret': settings.GITHUB_CLIENTSECRET,
        'redirect_uri': settings.GITHUB_CALLBACK,
        'state': _get_refer_url(request),
    }
    github_auth_url = '%s?%s' % (settings.GITHUB_AUTHORIZE_URL, parse.urlencode(data))
    print('git_hub_auth_url', github_auth_url)
    return HttpResponseRedirect(github_auth_url)


# github认证处理
def github_auth(request):
    template_html = 'account/login.html'

    # 如果申请登陆页面成功后，就会返回code和state(被坑了好久)
    if 'code' not in request.GET:
        return render(request, template_html)

    code = request.GET.get('code')

    # 第二步
    # 将得到的code，通过下面的url请求得到access_token
    url = 'https://github.com/login/oauth/access_token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.GITHUB_CLIENTID,
        'client_secret': settings.GITHUB_CLIENTSECRET,
        'code': code,
        'redirect_uri': settings.GITHUB_CALLBACK,
    }

    data = parse.urlencode(data)

    # 请求参数需要bytes类型
    binary_data = data.encode('utf-8')
    print('data:', data)

    # 设置请求返回的数据类型
    headers = {'Accept': 'application/json'}
    req = lib_request.Request(url, binary_data, headers)
    print('req:', req)
    response = lib_request.urlopen(req)
    result = response.read().decode('utf-8')
    # json是str类型的，将bytes转成str
    result = result.decode('ascii')
    result = json.loads(result)
    access_token = result['access_token']
    # print('access_token:', access_token)

    url = 'https://api.github.com/user?access_token=%s' % (access_token)
    response = lib_request.urlopen(url)
    html = response.read()
    html = html.decode('ascii')
    data = json.loads(html)
    username = data['name']
    # print('username:', username)
    password = '111111'

    # 如果不存在username，则创建
    try:
        user = Ouser.objects.get(username=username)
    except:
        user = Ouser.objects.create_user(username=username, password=password)
        user.save()

    # 登陆认证
    user = authenticate(username=username, password=password)
    login(request, user)
    return HttpResponseRedirect(reverse('index'))
