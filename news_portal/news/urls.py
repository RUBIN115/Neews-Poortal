from django.urls import path
from .views import (
   NewsList, NewDetail, SearchNewsList, AddNew, UpdateNew, DeleteNew,
   CategoryList, CategoryDetail, subscribe, unsubscribe
)
# from .views import IndexView


urlpatterns = [
   path('', NewsList.as_view(),
name='news'),
   path('<int:pk>', NewDetail.as_view(),
name='new'),
   path('search/', SearchNewsList.as_view(),
name='news_search'),
   path('add/', AddNew.as_view(),
name='new_add'),
   path('update/<int:pk>', UpdateNew.as_view(),
name='new_update'),
   path('delete/<int:pk>', DeleteNew.as_view(),
name='new_delete'),
   path('categories', CategoryList.as_view(),
name='categories'),
   path('categories/<int:pk>/', CategoryDetail.as_view(),
name='one_category'),
   path('categories/<int:pk>/subscribe/', subscribe,
name='subscribe'),
   path('categories/<int:pk>/unsubscribe/', unsubscribe,
name='unsubscribe'),
   # path('', IndexView.as_view()),
]