FROM        ubuntu:16.04
MAINTAINER  seungyun0914@gmail.com

# 현재 경로의 모든 파일들을 컨테이너의 /srv/picky폴더에 복사
COPY        . /srv/picky
# cd srvpicky와 같은 효과
WORKDIR     /srv/picky
# requirements 설치
RUN         /root/.pyenv/versions/picky/bin/pip install -r .requirements/deploy.txt

# RUN        /root/.pyenv/versions/picky/bin/uwsgi --http :8000 --chdir /srv/picky/django_app -w config.settings.debug

COPY        .config/supervisor/uwsgi.conf /etc/supervisor/conf.d/
COPY        .config/supervisor/nginx.conf /etc/supervisor/conf.d/


COPY        .config/nginx/nginx.conf /etc/nginx/nginx.conf
COPY        .config/nginx/nginx-app.conf /etc/nginx/sites-available/nginx-app.conf
RUN         rm -rf /etc/nginx/sites-enabled/default
RUN         ln -sf /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/nginx-app.conf


RUN         /root/.pyenv/versions/picky/bin/python /srv/picky/django_app/manage.py collectstatic --settings=config.settings.deploy --noinput
CMD         supervisord -n
#EXPOSE      80 8000