# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import (Toolview, BD_pushview, bd_api_view, BD_pushview_site, bd_api_site, Link_testview,
                    Link_test_api, regexview, regex_api, useragent_view, useragent_api, html_characters, verb_deformed,
                    verb_deformed, verb_deformed_view, adje_deformed, adje_deformed_view)

urlpatterns = [
    url(r'^$', Toolview, name='total'),  # 工具汇总页
    url(r'^baidu-linksubmit/$', BD_pushview, name='baidu_push'),  # 百度主动推送
    url(r'^verb_deformed/$', verb_deformed, name='verb_deformed'),  # 动词变换
    url(r'^verb_deformed_python/$', verb_deformed_view, name='verb_deformed_api'),
    url(r'^adje_deformed/$', adje_deformed, name='adje_deformed'),  # 形容词变换
    url(r'^adje_deformed_python/$', adje_deformed_view, name='adje_deformed_api'),
    url(r'^baidu-linksubmit/ajax/$', bd_api_view, name='baidu_push_api'),  # 百度推送ajax
    url(r'^baidu-linksubmit-for-sitemap/$', BD_pushview_site, name='baidu_push_site'),  # 百度主动推送sitemap
    url(r'^baidu-linksubmit-for-sitemap/ajax/$', bd_api_site, name='baidu_push_api_site'),
    url(r'^link-test/$', Link_testview, name='link_test'),  # 友链检测
    url(r'^link-test/ajax/$', Link_test_api, name='link_test_api'),
    url(r'^regex/$', regexview, name='regex'),  # 正则表达式在线
    url(r'^regex/ajax/$', regex_api, name='regex_api'),
    url(r'^user-agent/$', useragent_view, name='useragent'),  # user-agent生成器
    url(r'^user-agent/ajax/$', useragent_api, name='useragent_api'),
    url(r'^html-special-characters/$', html_characters, name='html_characters'),  # HTML特殊字符查询
]
