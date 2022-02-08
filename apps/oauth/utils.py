# -*- coding:UTF-8 -*-
# @Time : 2022/2/8 13:53
# @Author : Palm
# @Remark :
from urllib.parse import urlencode
from django.conf import settings
import logging

logger = logging.getLogger('django')


class OAuthGithub(object):
    """
    Github认证辅助工具类
    """

    # 初始化属性，接收四个参数，客户的appid，appkey，回调地址，初始跳转页面
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        # or：代表if not ，如果接收到参数值，就是用接收的，如果接收none，就用配置的
        self.client_id = client_id or settings.QQ_CLIENT_ID
        self.client_secret = client_secret or settings.QQ_CLIENT_SECRET
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URI
        self.state = state or settings.QQ_STATE  # 用于保存登录成功后的跳转页面路径

    # 定义生成url登录地址的函数，返回登录页面url的函数
    def get_github_login_url(self):
        """
        获取qq登录的网址
        :return: url网址
        """
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state,
            'scope': 'get_user_info',
        }
        url = 'https://graph.github.com/oauth2.0/authorize?' + urlencode(params)
        return url
