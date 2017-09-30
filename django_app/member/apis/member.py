from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.mail import send_mail, utils
from django.http import HttpResponse
from django.template import loader

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.base import EMAIL_HOST_USER
from member.models.pickyuser import PickyUserPasswordReset
from utils.permissions import ObjectIsMe
from ..serializers import (
    PickyUserSerializer,
    PickyUserCreateSerializer,
    PickyUserUpdateSerializer
)

PickyUser = get_user_model()

__all__ = (
    'PickyUserList',
    'PickyUserDetail',
    'PickyUserCreate',
    'PickyUserLogout',
    'PickyUserUpdate',
    'PickyUserFindPassword',
    'PickUserPasswordConfirm',
)


# user list / test 용도 8/2 Joe
# postman, 배포환경에서 정상작동 확인 8/4 Joe
class PickyUserList(generics.ListAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserSerializer


# postman, 배포환경에서 정상작동 확인 8/7 Joe
# permissions ObjectIsMe 추가 8/17 hong
class PickyUserDetail(generics.RetrieveAPIView):
    serializer_class = PickyUserSerializer
    permission_classes = (permissions.IsAuthenticated, ObjectIsMe)
    queryset = PickyUser.objects.all()


# 회원정보 부분 업데이트 8/12 joe / user permission 만들어야할것 같음.
# permissions ObjectIsMe 추가 8/17 hong
class PickyUserUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    PATCH : 수정
    DELETE : 삭제
    """
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserUpdateSerializer
    permission_classes = (permissions.IsAuthenticated, ObjectIsMe)

    def delete(self, request, *args, **kwargs):
        d = dict()
        d['result'] = '탈퇴되었습니다.'
        self.destroy(request, *args, **kwargs)
        return Response(d)


# 유저 생성(회원가입) 정상 작동함 8/10 joe
class PickyUserCreate(generics.CreateAPIView):
    queryset = PickyUser.objects.all()
    serializer_class = PickyUserCreateSerializer


class PickyUserLogout(generics.DestroyAPIView):
    queryset = PickyUser.objects.all()
    permission_classes = (permissions.IsAuthenticated, ObjectIsMe)

    def post(self, request, *args, **kwargs):
        d = dict()
        d['result'] = '로그아웃 되었습니다.'
        request.user.auth_token.delete()
        return Response(d)


# password 재설정 메일 발송
class PickyUserFindPassword(APIView):

    def post(request, user_email):
        email = user_email.POST['user_email']
        d = dict()
        try:
            user = PickyUser.objects.get(email=email)
        except Exception:
            d['email_error'] = '일치하는 아이디가 없습니다.'
            return Response(d)
        else:
            try:
                password_reset = PickyUserPasswordReset.objects.filter(user_id=user.pk)
            except PickyUserPasswordReset.DoesNotExist:
                password_reset = PickyUserPasswordReset.objects.create(
                        user_id=user.pk,
                )
            else:
                password_reset.delete()
                password_reset = PickyUserPasswordReset.objects.create(
                        user_id=user.pk,
                )

            html_message = loader.render_to_string(
                    'member/password_reset_email.html', {
                        'user': user.nickname,
                        'reset_link': password_reset.reset_link,
                    }
            )
            send_mail(
                    subject='Picky Cookbook 패스워드 재설정입니다.',
                    message='test message',
                    html_message=html_message,
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[email,],
                    fail_silently=False,
            )
            d['email_sent'] = '패스워드 재설정 이메일을 발송했습니다.'
            return Response(d)


class PickUserPasswordConfirm(APIView):

    def get(request, *args, **kwargs):
        d = dict()
        link = request.args[0]
        current_time = datetime.now()
        try:
            password_reset = PickyUserPasswordReset.objects.get(reset_link=link)
        except PickyUserPasswordReset.DoesNotExist:
            d['DoesNotExist'] = "존재하지 않는 링크입니다."
        else:
            if password_reset.used != 'n':
                d['used_link'] = "이미 사용된 링크입니다."
            elif current_time > password_reset.expired_date:
                d['expired_link'] = "만료된 링크입니다."
            else:
                password_reset.used = 'y'
                password_reset.save()
                d['email'] = PickyUser.objects.get(pk=password_reset.user_id).email
        return Response(d)

