from django.urls import path
from . import views

app_name = 'pirostagram'

urlpatterns = [
    # 1. 메인 피드 (홈 화면)
    path('', views.index, name='index'),
    
    # 2. 유저 검색 화면
    path('search/', views.user_search, name='user_search'),
    
    # 3. 프로필 화면
    path('profile/<str:username>/', views.profile, name='profile'),
    
    # 4. 게시글 생성
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    
    # 5. 게시글 수정
    path('post/<int:post_id>/update/', views.post_update, name='post_update'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),    

    # 6. 좋아요 
    path('post/<int:post_id>/like/', views.post_like_toggle, name='post_like_toggle'),
    
    # 7. 댓글 
    path('post/<int:post_id>/comment/create/', views.comment_create, name='comment_create'),
    path('comment/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

    # 8. 스토리 생성
    path('story/create/', views.story_create, name='story_create'),

    #9. 팔로우 토글
    path('profile/<int:user_id>/follow/', views.toggle_follow, name='toggle_follow'),

    
]