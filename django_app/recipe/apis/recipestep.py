from rest_framework import generics
from rest_framework import permissions

from recipe.models import RecipeStep
from recipe.serializers import RecipeStepCreateSerializer
from recipe.serializers import RecipeModifySerializer
from recipe.serializers import RecipeStepListSerializer
from utils.permissions import ObjectIsRequestUser, ObjectIsRequestRecipeStep


__all__ = (
    'RecipeStepCreateForFDS',
    'RecipeStepModifyDeleteView',
)

# recipecreateview 생성 - hong 8/1
# class RecipeStepCreateView(generics.CreateAPIView):
#     queryset = RecipeStep.objects.all()
#     permission_classes = (permissions.IsAuthenticated, ObjectIsRequestUser,)
#     serializer_class = RecipeStepCreateSerializer


# FDS용 레시피 생성. http 요청에 recipe pk 같이 올 예정.
# 이후 추가 작업 필요 8/9 joe
class RecipeStepCreateForFDS(generics.CreateAPIView):
    queryset = RecipeStep.objects.all()
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestUser,)
    serializer_class = RecipeStepCreateSerializer

    # def perform_create(self, serializer):
    #     serializer.save(
    #             user=self.request.user,
    #     )


# 승팔씀
class RecipeStepModifyDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeStep.objects.all()
    # 로그인 한 유저이며 레시피 스탭을 쓴사람과 현재 접속한 유저가 같을경우 수정 삭제가능
    # 인증관련부분은 ObjectsIsRequestRecipeStep 참조
    permission_classes = (permissions.IsAuthenticated, ObjectIsRequestRecipeStep,)

    # delete는 시리얼라이저를 쓸필요가 없음
    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return RecipeModifySerializer
