"""
Django settings for izone project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys
from .database_config import *
# 更换默认的数据库连接
import pymysql
from django.utils.translation import ugettext_lazy as _

pymysql.install_as_MySQLdb()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#!kta!9e0)24d@9#<*=ra$r!0k0+p8@w+a%7g1bbof0+ad@4_('

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 添加 apps 目录
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# 自由选择需要开启的功能
# 是否开始[在线工具]应用
TOOL_FLAG = True
# 是否开启[API]应用
API_FLAG = False
# DEBUG模式是否开始的选择
# 值为0：所有平台关闭DEBUG,值为1:所有平台开启DEBUG,值为其他：根据平台类型判断开启（默认设置的Windows下才开启）
DEBUG = debug_type

ALLOWED_HOSTS = ['*']

# Application definition

# 添加了新的app需要重启服务器
INSTALLED_APPS = [
    'bootstrap_admin',  # 注册bootstrap后台管理界面,这个必须放在最前面

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # 添加人性化过滤器
    'django.contrib.sitemaps',  # 网站地图

    'oauth',  # 自定义用户应用
    # allauth需要注册的应用
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.weibo',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.weixin',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'mdeditor',
    'rest_framework',

    'crispy_forms',  # bootstrap表单样式
    'imagekit',  # 上传图片的应用

    'haystack',  # 全文搜索应用 这个要放在其他应用之前
    'blog',  # 博客应用
    'tool',  # 工具
    'comment',  # 评论
]


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 工具条功能
        'height': 300,  # 编辑器高度
        'width': 800,  # 编辑器宽
    },
}

# 自定义用户model
AUTH_USER_MODEL = 'oauth.Ouser'

# allauth配置
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# allauth需要的配置
# 当出现"SocialApp matching query does not exist"这种报错的时候就需要更换这个ID
SITE_ID = 2

# 设置登录和注册成功后重定向的页面，默认是/accounts/profile/
LOGIN_REDIRECT_URL = "/"

# Email setting
# imoprt from base_settings more infos
# 禁用注册邮箱验证
ACCOUNT_EMAIL_VERIFICATION = 'none'
# 登录方式，选择用户名或者邮箱都能登录
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# 设置用户注册的时候必须填写邮箱地址
ACCOUNT_EMAIL_REQUIRED = True
# 登出直接退出，不用确认
ACCOUNT_LOGOUT_ON_GET = True

# 表单插件的配置
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LANGUAGES = (
    ('zh-hans', '简体中文'),
    ('zh-hant', '繁体中文')
)

ROOT_URLCONF = 'izone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 设置视图
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'blog.context_processors.settings_info',  # 自定义上下文管理器
            ],
        },
    },
]

WSGI_APPLICATION = 'izone.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 关闭国际时间，不然数据库报错

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# 静态文件收集
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'apps/blog/static'),
    os.path.join(BASE_DIR, 'apps/comment/static'),
    os.path.join(BASE_DIR, 'apps/tool/static'),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# 媒体文件收集
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CKEDITOR_JQUERY_URL = 'https://cdn.bootcss.com/jquery/2.1.4/jquery.js'
# CKEDITOR_IMAGE_BACKEND = "pillow"
# CKEDITOR_UPLOAD_PATH = os.path.join(BASE_DIR, 'media/upload')

# 统一分页设置
BASE_PAGE_BY = 10
BASE_ORPHANS = 5

# 全文搜索应用配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'blog.whoosh_cn_backend.WhooshEngine',  # 选择语言解析器为自己更换的结巴分词
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),  # 保存索引文件的地址，选择主目录下，这个会自动生成
    }
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 使用django-redis缓存页面，缓存配置如下：
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# restframework settings
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.AllowAny',
#     ),
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
#     'PAGE_SIZE': 20
# }

# 配置数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 修改数据库为MySQL，并进行配置
        'NAME': data_config.get("DATANAME"),  # 数据库的名称
        'USER': data_config.get("DATAUSER"),  # 数据库的用户名
        'PASSWORD': data_config.get("DATAPASS"),  # 数据库的密码
        'HOST': data_config.get("DATAHOST"),
        'PORT': data_config.get("DATAPORT"),
        'OPTIONS': {'charset': 'utf8', }
    }
}

# 邮箱配置
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = 'palm0318@163.com'
EMAIL_HOST_PASSWORD = 'LZBCWLGMAOTARKKV'  # 这个不是邮箱密码，而是授权码
EMAIL_PORT = 465  # 由于阿里云的25端口打不开，所以必须使用SSL然后改用465端口
# 是否使用了SSL 或者TLS，为了用465端口，要使用这个
EMAIL_USE_SSL = True
EMAIL_USE_TLS = True
# 默认发件人，不设置的话django默认使用的webmaster@localhost，所以要设置成自己可用的邮箱
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# 网站默认设置和上下文信息
SITE_END_TITLE = _('霓虹Study')
SITE_DESCRIPTION = _('本站专注于日语学习，站长本人也在学习日语，本站提供了日语中动词变形，形容词变形小工具，日语学习资料，日语听力资料，日语面试情景对话等内容')
SITE_KEYWORDS = _('日语初学者,日语学习资料,日语考试听力,日语动词变形,日语备考')
SITE_TITLE = _('一个适合日语初学者的博客')
