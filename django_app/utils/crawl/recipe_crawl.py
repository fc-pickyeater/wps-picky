import re
from tempfile import NamedTemporaryFile

import requests
from IPython.utils.data import flatten
from bs4 import BeautifulSoup
from django.core.files import File
from selenium import webdriver

from member.models import PickyUser
from recipe.models import Recipe
from recipe.models import RecipeStep


class RecipeCrawler:
    _url_base = 'http://post.naver.com/viewer/postView.nhn?volumeNo={recipe_num}&memberNo=1267558&pageType=detail&commentGroupId=1267558&commentObjectId=8409091_1267558&contentsId=136696&requestQueryString=rid%3D2212%26attrId%3D%26contents_id%3D136696%26leafId%3D1081'

    def crawl_recipe(self, recipe_num=None):
        url_recipe = self._url_base.format(
            recipe_num=recipe_num
        )

        driver = webdriver.PhantomJS(
            '/Users/hongdonghyun/projects/team_project/wps-picky/django_app/utils/crawl/phantomjs')
        driver.get(url_recipe)

        html = driver.page_source
        soup = BeautifulSoup(html)

        # 전체 페이지에서 타이틀 부분 뽑아옴
        title = soup.select_one('title').get_text()
        title_list = title.split(':')
        empty_list = []
        for t in title_list:
            t = t.strip(' ')
            empty_list.append(t)

        # 레시피의 이미지 뽑아옴
        div_editor = soup.find("div", {"class": "edtitor_img_uio"})
        recipe_img = div_editor.img['src']

        # 레시피의 타이틀, 설명 뽑아옴
        recipe_title = empty_list[0]
        recipe_description = empty_list[1]

        div_container_inner = soup.find("div", {"class": "__viewer_container_inner"})
        div_na_summary_info = div_container_inner.find_all("div", {"class": "na_summary_info"})

        # select함수는 리턴값이 리스트형식
        _list = []
        for before_list in div_na_summary_info:
            a = before_list.select("ul > li > span")
            _list.append(a)

        # 위 과정을 거치면 이중 리스트 형식이됨

        # 이중 리스트 형식을 일자화 시키는 함수 flatten
        _list = flatten(_list)

        # 일자화된 리스트에서 span을 제외한 text값 추출
        # ingredient_list라는 변수에 할당
        ingredient_list = []
        for after_list in _list:
            ingredient = after_list.get_text()
            ingredient_list.append(ingredient)
        # ,로 join
        ingredient_list = ','.join(ingredient_list)

        # 스탭 부분 이미지
        div_tptype_5 = soup.find_all("div", {"class": "t_ptype5"})
        # 스탭 부분 텍스트
        div_p = soup.find_all("p", {"class": "t_txt"})

        # 스탭 이미지 추출
        img_list = []
        for image in div_tptype_5:
            img_list.append(image.img['src'])

        # 스탭 설명 추출
        text_list = []
        for text in div_p:
            text_list.append(text.get_text())
        del text_list[0]

        # 기존 텍스트에 \n,\t제거
        i = ' '.join(text_list).replace('\n', '')
        i = i.replace('\t', '')
        # STEP기준으로 설명을 쪼갠다
        # 이 기능에서 STEP삭제
        # 삭제를 위한 정규표현식
        pattern = re.compile(r'STEP \d+\s?')
        # text_list에 다시 대입
        # 공백제거, 만약 텍스트가 빈공백 요소일 경우 제거
        text_list = [text.strip() for text in pattern.split(i) if text]
        for text in text_list:
            # 크롤링 도중 원하지 않는 부분이 있어 제거하기 위한 if문
            if '(숫자)' in text:
                del text_list[0]

        # 임시 데이터의 File_name
        file_name = '{}.jpg'.format(recipe_title)
        # 무슨 기능을 하는지 확인필요 - hong 8/21
        temp_file = NamedTemporaryFile(delete=True)
        # response변수에 recipe_img 저장
        response = requests.get(recipe_img)
        # temp_file에 recipe_img의 content를 저장
        # 동작 후 사라지는 임시파일
        temp_file.write(response.content)

        # 레시피 생성
        _2bab_recipe = Recipe.objects.create(
            title=recipe_title,
            description=recipe_description,
            ingredient=ingredient_list,
            # 현재는 pickyuser 첫번째 유저를 가져오지만 최종 정리 후
            # admin의 아이디를 가져와야함 - hong 8/21
            user=PickyUser.objects.first()
        )

        # 위에서 저장한 임시파일을 _2bab_recipe의 이미지필드에 저장
        _2bab_recipe.img_recipe.save(file_name, File(temp_file))

        # zip으로 묶인 img_list 와 img에 대한 description_list
        for x, y in zip(img_list, text_list):
            # 위에서 만든 _2bab_recipe의 pk에 매핑
            # 설명을 저장 후 생성
            _2bab_recipe_step = RecipeStep.objects.create(description=y, recipe_id=_2bab_recipe.pk)
            # 상단의 동일코드와 같음
            # 설명생략
            file_name = '{}.{}.jpg'.format(_2bab_recipe.pk, recipe_title)
            temp_file = NamedTemporaryFile(delete=True)
            response = requests.get(x)
            temp_file.write(response.content)
            _2bab_recipe_step.img_step.save(file_name, File(temp_file))

        # print(recipe_title)
        # print(recipe_description)
        # print(recipe_img)
        # print(ingredient_list)
        # print(img_list)
        # print(text_list)


a = RecipeCrawler()

# for i in range(8408511, 8409092):
#     try:
#         a.crawl_recipe(i)
#     except:
#         pass

a.crawl_recipe(8409092)
