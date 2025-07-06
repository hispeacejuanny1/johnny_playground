from django.urls import path
from . import views

urlpatterns = [
    path('<str:board_type>/', views.post_list, name='post_list'),         # 목록
    path('<str:board_type>/<int:pk>/', views.post_detail, name='post_detail'),   # 상세
    path('<str:board_type>/write/', views.post_create, name='post_create'),      # 글쓰기
    path('<str:board_type>/<int:pk>/edit/', views.post_edit, name='post_edit'),  # 수정
    path('<str:board_type>/<int:pk>/delete/', views.post_delete, name='post_delete'), # 삭제
]
