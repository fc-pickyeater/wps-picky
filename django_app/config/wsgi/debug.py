import os

from django.core.wsgi import get_wsgi_application

# WSGI 구동 환경 기본값 지정 (debug 모드
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.debug")

# WSGI 사용
application = get_wsgi_application()
