import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers.login import FacebookLoginSerializer
from ..serializers import PickyAuthTokenSerializer

PickyUser = get_user_model()



# 로그인 view
# 토큰 검증
class ObtainAuthToken(APIView):
    # 공부가 필요
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = PickyAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        d = dict()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        d['token'] = token.key
        d['pk'] = user.pk
        return Response(d)


obtain_auth_token = ObtainAuthToken.as_view()


class FacebookLoginAPIView(APIView):
    # get_access_token은 생략됨(JavaScript SDK를 사용)
    # access token을 받은 이후 처리만 하면 됨
    app_access_token = '{}|{}'.format(
        settings.FACEBOOK_APP_ID,
        settings.FACEBOOK_SECRET_CODE,
    )

    def post(self, request):
        token = request.data.get('token')

        if not token:
            raise APIException('token required')

        # 프론트로부터 전달받은 token을 Facebook의 debug_token API를 사용해 검증한 결과를 debug_result에 할당
        self.debug_token(token)
        user_info = self.get_user_info(token=token)

        if PickyUser.objects.filter(fb_id=user_info['id']).exists():
            user = PickyUser.objects.get(fb_id=user_info['id'])
        else:
            user = PickyUser.objects.create_facebook_user(user_info)
        ret = FacebookLoginSerializer(user).data
        return Response(ret)

    def debug_token(self, token):
        url_debug_token = 'https://graph.facebook.com/debug_token'
        url_debug_token_params = {
            'input_token': token,
            'access_token': self.app_access_token,
        }
        response = requests.get(url_debug_token, url_debug_token_params)
        result = response.json()
        if 'error' in result or 'error' in result['data']:
            raise APIException('token이 유효하지 않습니다.')
        return result

    def get_user_info(self, token):
        url_user_info = 'https://graph.facebook.com/v2.9/me'
        url_user_info_params = {
            'access_token': token,
            'fields': ','.join([
                'id',
                'name',
                'email',
                'picture.type(large)',
            ])
        }
        response = requests.get(url_user_info, params=url_user_info_params)
        result = response.json()
        return result
