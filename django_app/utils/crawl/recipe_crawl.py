# from IPython.utils.data import flatten
# from bs4 import BeautifulSoup
# from selenium import webdriver
#
# from recipe.models import Recipe
#
#
# class RecipeCrawler:
#     _url_base = 'http://post.naver.com/viewer/postView.nhn?volumeNo={recipe_num}&memberNo=1267558&pageType=detail&commentGroupId=1267558&commentObjectId=8409091_1267558&contentsId=136696&requestQueryString=rid%3D2212%26attrId%3D%26contents_id%3D136696%26leafId%3D1081'
#
#     # 8409092
#
#     def crawl_recipe(self, recipe_num=None):
#         url_recipe = self._url_base.format(
#             recipe_num=recipe_num
#         )
#
#         driver = webdriver.PhantomJS(
#             '/Users/hongdonghyun/projects/team_project/wps-picky/django_app/utils/crawl/phantomjs')
#         driver.get(url_recipe)
#
#         html = driver.page_source
#         soup = BeautifulSoup(html)
#
#         # 전체 페이지에서 타이틀 부분 뽑아옴
#         title = soup.select_one('title').get_text()
#         title_list = title.split(':')
#         empty_list = []
#         for t in title_list:
#             t = t.strip(' ')
#             empty_list.append(t)
#
#         # 레시피의 이미지 뽑아옴
#         div_editor = soup.find("div", {"class": "edtitor_img_uio"})
#         recipe_img = div_editor.img['src']
#
#         # 레시피의 타이틀, 설명 뽑아옴
#         recipe_title = empty_list[0]
#         recipe_description = empty_list[1]
#
#         div_container_inner = soup.find("div", {"class": "__viewer_container_inner"})
#         div_na_summary_info = div_container_inner.find_all("div", {"class": "na_summary_info"})
#
#         # select함수는 리턴값이 리스트형식
#         _list = []
#         for before_list in div_na_summary_info:
#             a = before_list.select("ul > li > span")
#             _list.append(a)
#
#         # 위 과정을 거치면 이중 리스트 형식이됨
#
#         # 이중 리스트 형식을 일자화 시키는 함수 flatten
#         _list = flatten(_list)
#
#         # 일자화된 리스트에서 span을 제외한 text값 추출
#         # ingredient_list라는 변수에 할당
#         ingredient_list = []
#         for after_list in _list:
#             ingredient = after_list.get_text()
#             ingredient_list.append(ingredient)
#
#         # 스탭 부분 이미지
#         div_tptype_5 = soup.find_all("div", {"class": "t_ptype5"})
#         # 스탭 부분 텍스트
#         div_p = soup.find_all("p", {"class": "t_txt"})
#
#         img_list = []
#         for image in div_tptype_5:
#             img_list.append(image.img['src'])
#
#         text_list = []
#         for text in div_p:
#             text_list.append(text.get_text())
#         del text_list[0]
#
#         print(recipe_title)
#         print(recipe_description)
#         print(recipe_img)
#         print(ingredient_list)
#         print(img_list)
#         print(text_list)
#
#         Recipe.objects.create(title=recipe_title, description=recipe_description, ingredient=ingredient_list)
#
#
# a = RecipeCrawler()
# a.crawl_recipe(8409092)
