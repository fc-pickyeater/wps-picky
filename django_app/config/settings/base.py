"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/

'test'
"""
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)

# config_secret 폴더 및 하위 파일 경로
CONFIG_SECRET_DIR = os.path.join(ROOT_DIR, '.config_secret')
CONFIG_SECRET_COMMON_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_common.json')
CONFIG_SECRET_DEBUG_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_debug.json')
CONFIG_SECRET_DEPLOY_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_deploy.json')

# CORS setting
CORS_ORIGIN_WHITELIST = (
    'pickycookbook.co.kr',
    'ec2-13-124-185-153.ap-northeast-2.compute.amazonaws.com',
    'localhost:8000',
    'localhost:8080',
)

# CONFIG_SECRET_FILE 경로의 파일을 읽은값 할당
config_secret_common = json.loads(open(CONFIG_SECRET_COMMON_FILE).read())

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config_secret_common['django']['secret_key']

# User model
AUTH_USER_MODEL = 'member.PickyUser'

# Facebook
FACEBOOK_APP_ID = config_secret_common['facebook']['app_id']
FACEBOOK_SECRET_CODE = config_secret_common['facebook']['secret_code']

# Email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EAMIL_PORT = 25
EMAIL_HOST_USER = config_secret_common['email']['USER']
EMAIL_HOST_PASSWORD = config_secret_common['email']['PASSWORD']
DEFAULT_FROM_EMAIL = 'Picky Cookbook <help@pickycookbook.co.kr>'


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    ### add list ###
    # django_extensions는 debug 파일로 옮깁니다. 8/2 Joe
    # ----------------------------------------------------
    # crawling시 deploy에 shell_plus가 없어서 에러가 뜸
    # 다시 주석을 풀고 복구 시킴 8/21 hong
    'django_extensions',
    'rest_framework',
    'django_filters',
    # user token 생성용 8/4 Joe
    # token Table 생성
    'rest_framework.authtoken',

    # kakao login을 위한 django-allauth
    # 'django.contrib.sites',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.kakao',
    # 'allauth.socialaccount.providers.naver',

    'recipe',
    'ingredient',
    'member',
    'corsheaders',
]

# 'django.contrib.sites'를 사용할 경우 필요.
# 지정하지 않으면 요청시 host 명의 Site 인스턴스를 찾음.
# SITE_ID = 1

# 이메일확인을 하지않음. (이미 안보내고있긴함) 9/9 조
# SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'

# 8/1 hong 추가 search filter html보여주는듯? -hong 8/1
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    # token 기반인증을 위해 추가 8/7 joe
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'allauth.account.auth_backends.AuthenticationBackend',
    ),
    # 반환되는 JSON에 status_code를 같이 보내줌.
    'EXCEPTION_HANDLER': 'utils.exception_handler.custom_exception_handler',
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]
