import datetime
from xml import etree
import requests
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.html import mark_safe
from .apis.bd_push import push_urls, get_urls
from .apis.links_test import Check
from .apis.useragent import get_user_agent
from .c_list import *
import re
import markdown
from .models import ExamPlan


# Create your views here.

def Toolview(request):
    return render(request, 'tool/tool.html')


# 百度主动推送
def BD_pushview(request):
    return render(request, 'tool/bd_push.html')

def verb_deformed(request):
    return render(request, 'tool/verb_deformed.html')

def exam_time(request):
    # ExamPlan
    site_date = datetime.datetime.strptime('2021-12-5', '%Y-%m-%d')
    today = datetime.datetime.today()
    interval_days = (site_date - today).days
    return render(request, 'tool/exam_time.html', context={'interval_days':interval_days})

def adje_deformed(request):
    return render(request, 'tool/adje_deformed.html')

@require_POST
def bd_api_view(request):
    if request.is_ajax():
        data = request.POST
        url = data.get('url')
        urls = data.get('url_list')
        info = push_urls(url, urls)
        return JsonResponse({'msg': info})
    return JsonResponse({'msg': 'miss'})

@require_POST
def verb_deformed_view(request):
    verb_d = request.POST.get('verb_d')
    deform_what = request.POST.get('deform_what')
    if deform_what == "1":
        return JsonResponse({'msg': turn2real(verb_d)})
    if deform_what == "2":
        return JsonResponse({'msg': turn2masu(verb_d)})
    if deform_what == "3":
        return JsonResponse({'msg': turn2nai(verb_d)})
    if deform_what == "4":
        return JsonResponse({'msg': turn2te(verb_d)})
    if deform_what == "5":
        return JsonResponse({'msg': turn2ta(verb_d)})
    if deform_what == "6":
        return JsonResponse({'msg': turn2order(verb_d)})
    if deform_what == "7":
        return JsonResponse({'msg': turn2maybe(verb_d)})
    if deform_what == "8":
        return JsonResponse({'msg': turn2if(verb_d)})
    if deform_what == "9":
        return JsonResponse({'msg': turn2want(verb_d)})
    if deform_what == "10":
        return JsonResponse({'msg': turn2passive(verb_d)})
    if deform_what == "11":
        return JsonResponse({'msg': turn2use(verb_d)})
    if deform_what == "12":
        return JsonResponse({'msg': turn2useApassive(verb_d)})
    if deform_what == "13":
        return JsonResponse({'msg': turn2stop(verb_d)})
    return JsonResponse({'msg': 'miss'})

def turn2real(verb_d):
    return verb_d

def turn2masu(verb_d):
    type_ = verb_123(verb_d)
    if type_ == 1:
        last_c = verb_d[-1:]
        last_value_index = list(u_dict.values()).index(last_c)
        last_c_key = list(u_dict.keys())[last_value_index]
        i_value = i_dict.get(last_c_key)
        verb_d = verb_d[:-1] + i_value + "ます"
    elif type_ == 2:
        verb_d = verb_d[:-1] + "ます"
    else:
        if verb_d == "来る":
            verb_d = "来（き）ます"
        if verb_d[-2:] == "する":
            verb_d = verb_d[:-2] + "します"
    return verb_d

def turn2nai(verb_d):
    type_ = verb_123(verb_d)
    if type_ == 1:
        last_c = verb_d[-1:]
        last_value_index = list(u_dict.values()).index(last_c)
        last_c_key = list(u_dict.keys())[last_value_index]
        i_value = a_dict.get(last_c_key)
        if i_value == "あ":
            i_value = "わ"
        verb_d = verb_d[:-1] + i_value + "ない"
    if type_ == 2:
        verb_d = verb_d[:-1] + "ない"
    if type_ == 3:
        if verb_d == "来る":
            verb_d = "来(こ)ない"
        if verb_d[-2:] == "する":
            verb_d = verb_d[:-2] + "しない"
    return verb_d

def turn2te(verb_d):
    if verb_123(verb_d) == 1:
        if verb_d[-1] == "く":
            if verb_d == "行く":
                return "行って"
            else:
                return verb_d[:-1] + "い" + "て"
        elif verb_d[-1] == "ぐ":
            return verb_d[:-1] + "い" + "で"
        elif verb_d[-1] in ["ぶ", "む", "ぬ"]:
            return verb_d[:-1] + "ん" + "で"
        elif verb_d[-1] in ["つ", "る", "う"]:
            return verb_d[:-1] + "って"
        elif verb_d[-1] == "し":
            return verb_d + "て"
        elif verb_d[-1] == "す":
            return verb_d[:-1] + "して"
    elif verb_123(verb_d) == 2:
        return verb_d[:-1] + "て"
    elif verb_123(verb_d) == 3:
        if verb_d[-2:] == "する":
            return verb_d[:-2] + "して"
        return verb_d[:-1] + "て"

def turn2ta(verb_d):
    if verb_123(verb_d) == 1:
        if verb_d[-1] == "く":
            if verb_d == "行く":
                return "行った"
            else:
                return verb_d[:-1] + "い" + "た"
        elif verb_d[-1] == "ぐ":
            return verb_d[:-1] + "い" + "だ"
        elif verb_d[-1] in ["ぶ", "む", "ぬ"]:
            return verb_d[:-1] + "ん" + "だ"
        elif verb_d[-1] in ["つ", "る", "う"]:
            return verb_d[:-1] + "った"
        elif verb_d[-1] == "し":
            return verb_d + "た"
        elif verb_d[-1] == "す":
            return verb_d[:-1] + "した"
    elif verb_123(verb_d) == 2:
        return verb_d[:-1] + "た"
    elif verb_123(verb_d) == 3:
        if verb_d[-2:] == "する":
            return verb_d[:-2] + "した"
        return verb_d[:-1] + "た"

def turn2order(verb_d):
    type_ = verb_123(verb_d)
    if type_ == 1:
        last_c = verb_d[-1:]
        last_value_index = list(u_dict.values()).index(last_c)
        last_c_key = list(u_dict.keys())[last_value_index]
        i_value = e_dict.get(last_c_key)
        verb_d = verb_d[:-1] + i_value
    if type_ == 2:
        verb_d = verb_d[:-1] + "ろ"
    if type_ == 3:
        if verb_d == "来る":
            verb_d = "来（こ）い"
        elif verb_d[-2:] == "する":
            verb_d = verb_d[:-2] + "しろ"
    return verb_d

def turn2maybe(verb_d):
    type_ = verb_123(verb_d)
    if type_ == 1:
        last_c = verb_d[-1:]
        last_value_index = list(u_dict.values()).index(last_c)
        last_c_key = list(u_dict.keys())[last_value_index]
        i_value = e_dict.get(last_c_key)
        verb_d = verb_d[:-1] + i_value + "る"
    if type_ == 2:
        verb_d = verb_d[:-1] + "られる"
    if type_ == 3:
        if verb_d == "来る":
            verb_d = "来（こ）られる"
        if verb_d[-2:] == "する":
            verb_d = verb_d[:-2] + "できる"
    return verb_d

def turn2if(verb_d):
    type_ = verb_123(verb_d)
    if type_ == 1:
        last_c = verb_d[-1:]
        last_value_index = list(u_dict.values()).index(last_c)
        last_c_key = list(u_dict.keys())[last_value_index]
        i_value = e_dict.get(last_c_key)
        verb_d = verb_d[:-1] + i_value + "ば"
    if type_ == 2:
        verb_d = verb_d[:-1] + "れば"
    if type_ == 3:
        if verb_d == "来る":
            verb_d = "来（く）れば"
        if verb_d[-2:] == "する":
            verb_d = verb_d[:-2] + "すれば"
    return verb_d

def turn2want(verb_d):
    type_ = verb_123(verb_d)
    if type_ == 1:
        last_c = verb_d[-1:]
        last_value_index = list(u_dict.values()).index(last_c)
        last_c_key = list(u_dict.keys())[last_value_index]
        i_value = o_dict.get(last_c_key)
        verb_d = verb_d[:-1] + i_value + "う"
    if type_ == 2:
        verb_d = verb_d[:-1] + "よう"
    if type_ == 3:
        if verb_d == "来る":
            verb_d = "来（こ）よう"
        elif verb_d[-2:] == "する":
            verb_d = verb_d[:-2] + "しよう"
    return verb_d

def turn2use(verb_d):
    type_ = verb_123(verb_d)
    if type_ == 1:
        last_c = verb_d[-1:]
        last_value_index = list(u_dict.values()).index(last_c)
        last_c_key = list(u_dict.keys())[last_value_index]
        i_value = a_dict.get(last_c_key)
        if i_value == "あ":
            i_value = "わ"
        verb_d = verb_d[:-1] + i_value + "せる"
    if type_ == 2:
        verb_d = verb_d[:-1] + "させる"
    if type_ == 3:
        if verb_d == "来る":
            verb_d = "来（こ）させる"
        if verb_d[-2:] == "する":
            verb_d = verb_d[:-2] + "させる"
    return verb_d

def turn2passive(verb_d):
    type_ = verb_123(verb_d)
    if type_ == 1:
        last_c = verb_d[-1:]
        last_value_index = list(u_dict.values()).index(last_c)
        last_c_key = list(u_dict.keys())[last_value_index]
        i_value = a_dict.get(last_c_key)
        if i_value == "あ":
            i_value = "わ"
        verb_d = verb_d[:-1] + i_value + "れる"
    if type_ == 2:
        verb_d = verb_d[:-1] + "られる"
    if type_ == 3:
        if verb_d == "来る":
            verb_d = "来（こ）られる"
        elif verb_d[-2:] == "する":
            verb_d = verb_d[:-2] + "される"
    return verb_d

def turn2useApassive(verb_d):
    type_ = verb_123(verb_d)
    if type_ == 1:
        last_c = verb_d[-1:]
        last_value_index = list(u_dict.values()).index(last_c)
        last_c_key = list(u_dict.keys())[last_value_index]
        i_value = a_dict.get(last_c_key)
        if i_value == "あ":
            i_value = "わ"
        verb_d = verb_d[:-1] + i_value + "される"
    if type_ == 2:
        verb_d = verb_d[:-1] + "させられる"
    if type_ == 3:
        if verb_d == "来る":
            verb_d = "来（こ）させられる"
        elif verb_d[-2:] == "する":
            verb_d = verb_d[:-2] + "させられる"
    return verb_d

def turn2stop(verb_d):
    return verb_d + "な"

@require_POST
def adje_deformed_view(request):
    adje_d = request.POST.get('adje_d')
    deform_what = request.POST.get('deform_what')
    if deform_what == "1":
        return JsonResponse({'msg': jian_1_1(adje_d)})
    if deform_what == "2":
        return JsonResponse({'msg': jing_1_1(adje_d)})
    if deform_what == "3":
        return JsonResponse({'msg': jian_0_1(adje_d)})
    if deform_what == "4":
        return JsonResponse({'msg': jing_0_1(adje_d)})
    if deform_what == "5":
        return JsonResponse({'msg': jian_1_0(adje_d)})
    if deform_what == "6":
        return JsonResponse({'msg': jing_1_0(adje_d)})
    if deform_what == "7":
        return JsonResponse({'msg': jian_0_0(adje_d)})
    if deform_what == "8":
        return JsonResponse({'msg': jing_0_0(adje_d)})
    return JsonResponse({'msg': 'miss'})

def exam_time_view(request):
    today = datetime.date.today()
    print(today)
    pass

def detect_adje(word):
    if word[-1] != "い":
        return 2
    else:
        return 1

def jian_1_1(adje_d):
    # 简体肯定现在
    if detect_adje(adje_d) == 1:
        return adje_d
    else:
        return adje_d+"だ"

def jing_1_1(adje_d):
    # 敬体肯定现在
    return adje_d + "です"

def jian_0_1(adje_d):
    # 简体否定现在
    if detect_adje(adje_d) == 1:
        return adje_d[:-1]+"くない"
    else:
        return [adje_d + "ではない"," / ", adje_d + "じゃない"]
def jing_0_1(adje_d):
    # 敬体否定现在
    if detect_adje(adje_d) == 1:
        return [adje_d[:-1]+"くないです", " / ", adje_d[:-1]+"くありません"]
    else:
        return [adje_d + "では(じゃ)ありません"," / ", adje_d + "では(じゃ)ないです"]

def jian_1_0(adje_d):
    # 简体肯定过去
    if detect_adje(adje_d) == 1:
        return adje_d[:-1] + "かった"
    else:
        return adje_d + "だった"

def jing_1_0(adje_d):
    # 敬体肯定过去
    if detect_adje(adje_d) == 1:
        return adje_d[:-1] + "かったです"
    else:
        return adje_d + "でした"

def jian_0_0(adje_d):
    # 简体否定过去
    if detect_adje(adje_d) == 1:
        return adje_d[:-1]+"くなかた"
    else:
        return [adje_d+"ではなかった", " / ", adje_d+"じゃなかった"]

def jing_0_0(adje_d):
    # 敬体否定过去
    if detect_adje(adje_d) == 1:
        return [adje_d[:-1]+"くなかったです", " / ", adje_d[:-1]+"くありませんでした"]
    else:
        return [adje_d+"では(じゃ)ありませんでした", " / ", adje_d+"では(じゃ)なかったです"]

def verb_123(verb_d):
    last_c = verb_d[-1:]
    if last_c in u_list:
        return 1
    if last_c == "る" and verb_d not in ["来る", "くる"] and verb_d[-2:] != "する":
        last_cc = verb_d[-2:-1]
        if last_cc not in all_list:
            verb_d = duyin(verb_d)
            last_cc = verb_d[-2:-1]
        if last_cc in o_list + a_list+u_list or verb_d in YILEITESHU:
            return 1
        if last_cc in i_list + e_list and verb_d not in YILEITESHU:
            return 2

    if verb_d[-2:] == "する":
        return 3
    if verb_d[-2:] == "来る" or verb_d[-2:] == "くる":
        return 3

def duyin(word):
    url = "https://ja.wiktionary.org/wiki/%s" % word
    response = requests.get(url)
    dom = etree.HTML(response.text)
    t = dom.xpath('//div[@class="mw-parser-output"]')
    duyin_ = t[0].xpath('ol/li/b/a[1]')[0].text
    return duyin_

# 百度主动推送升级版，提取sitemap链接推送
def BD_pushview_site(request):
    return render(request, 'tool/bd_push_site.html')


@require_POST
def bd_api_site(request):
    if request.is_ajax():
        data = request.POST
        url = data.get('url')
        map_url = data.get('map_url')
        urls = get_urls(map_url)
        if urls == 'miss':
            info = "{'error':404,'message':'sitemap地址请求超时，请检查链接地址！'}"
        elif urls == '':
            info = "{'error':400,'message':'sitemap页面没有提取到有效链接，sitemap格式不规范。'}"
        else:
            info = push_urls(url, urls)
        return JsonResponse({'msg': info})
    return JsonResponse({'msg': 'miss'})


# 友链检测
def Link_testview(request):
    return render(request, 'tool/link_test.html')


@require_POST
def Link_test_api(request):
    if request.is_ajax():
        data = request.POST
        p = data.get('p')
        urls = data.get('urls')
        c = Check(urls, p)
        info = c.run()
        return JsonResponse(info)
    return JsonResponse({'msg': 'miss'})


# 在线正则表达式
def regexview(request):
    return render(request, 'tool/regex.html')


@require_POST
def regex_api(request):
    if request.is_ajax():
        data = request.POST
        texts = data.get('texts')
        regex = data.get('r')
        try:
            lis = re.findall(r'{}'.format(regex), texts)
        except:
            lis = []
        num = len(lis)
        info = '\n'.join(lis)
        result = "匹配到&nbsp;{}&nbsp;个结果：\n".format(num) + "```\n" + info + "\n```"
        result = markdown.markdown(result, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        return JsonResponse({'result': mark_safe(result), 'num': num})
    return JsonResponse({'msg': 'miss'})


# 生成请求头
def useragent_view(request):
    return render(request, 'tool/useragent.html')


@require_POST
def useragent_api(request):
    if request.is_ajax():
        data = request.POST
        d_lis = data.get('d_lis')
        os_lis = data.get('os_lis')
        n_lis = data.get('n_lis')
        d = d_lis.split(',') if len(d_lis) > 0 else None
        os = os_lis.split(',') if len(os_lis) > 0 else None
        n = n_lis.split(',') if len(n_lis) > 0 else None
        result = get_user_agent(os=os, navigator=n, device_type=d)
        return JsonResponse({'result': result})
    return JsonResponse({'msg': 'miss'})


# HTML特殊字符对照表
def html_characters(request):
    return render(request, 'tool/characters.html')
