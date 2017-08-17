from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions

from ingredient.models import Ingredient
from ingredient.serializers.ingredient import IngredientSerializer
from utils.permissions import ObjectIsRequestUser

__all__ = (
    'IngredientSearchListCreateView',
    'IngredientModifyDeleteView',
)


# ingredient search and list post요청시 생성 get요청시 list postman 확인 - hong 8/1
class IngredientSearchListCreateView(generics.ListCreateAPIView):
    """
    POST GET
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # 인증 관련부분
    # 인증이 통과 되지 못하면 readonly(get요청)
    # 인증을 하는 부분은 ObjectsIsRequestUser을 참조
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ObjectIsRequestUser,)
    # url에 ingredient/?name= 검색할거 입력
    filter_backends = (filters.DjangoFilterBackend,)
    # url parameter붙는 부분을 여기서 정함
    filter_fields = ('name',)

    def get_serializer_class(self):
        # post요청시 생성
        if self.request.method == 'POST':
            return IngredientSerializer
        # get요청시 리스트
        elif self.request.method == 'GET':
            return IngredientSerializer

    # post요청시 생성할 때 user에 현재접속한 유저값을 넣음
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ingredient modify and delete patch요청시 수정 delete요청시 삭제 postman 확인 - hong 8/1
class IngredientModifyDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    PATCH DELETE
    """
    queryset = Ingredient.objects.all()
    # 인증관련 부분
    # SearchListCreateView랑 인증이 다름
    # 인증을 통과한 사람만 삭제 수정이 가능함
    # 인증을 하는 부분은 ObjectsIsRequestUser을 참조
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestUser,)
    serializer_class = IngredientSerializer

