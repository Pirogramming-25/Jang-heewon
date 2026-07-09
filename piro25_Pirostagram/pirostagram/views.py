from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Post, Comment, PostLike, Story, Follow, Comment
from django.contrib.auth.decorators import login_required
from django.db.models import Count

# 메인화면 피드 
def index(request):
    sort_by = request.GET.get('sort', 'latest')
    queryset = Post.objects.annotate(like_count=Count('likes'))
    if sort_by == 'like':
        posts = Post.objects.annotate(like_count_attr=Count('postlike')).order_by('-like_count_attr', '-id')
    elif sort_by == 'content':
        posts = queryset.order_by('content')
    else:
        posts = queryset.order_by('-created_at')

    post_list = []
    for post in posts:
        like_count = PostLike.objects.filter(post=post).count()
        
        is_liked = False
        if request.user.is_authenticated:
            is_liked = PostLike.objects.filter(post=post, user=request.user).exists()

        comments = Comment.objects.filter(post=post).order_by('created_at')
            
        post_list.append({
            'post_obj': post,
            'like_count': like_count,
            'is_liked': is_liked,
            'comments': comments,
        })

    suggested_users = User.objects.exclude(username=request.user.username)[:4] if request.user.is_authenticated else User.objects.all()[:4]
    active_stories = Story.objects.all().order_by('-created_at')
    context = {
        'post_list': post_list,
        'suggested_users': suggested_users,
        'stories': active_stories,
    }
    return render(request, 'pirostagram/index.html', context)

# 프로필 
def profile(request, username):
    target_user = get_object_or_404(User, username=username)
    user_posts = target_user.posts.all().order_by('-created_at')
    follower_count = target_user.followers.all().count() 
    following_count = target_user.following.all().count()
    
    context = {
        'target_user': target_user,
        'user_posts': user_posts,
        'post_count': user_posts.count(),
        'follower_count': follower_count,
        'following_count': following_count,
    }
    return render(request, 'pirostagram/profile.html', context)

# 유저 검색 
def user_search(request):
    query = request.GET.get('search_word', '')
    
    if query:
        users = User.objects.filter(username__icontains=query)
    else:
        users = User.objects.none()
        
    search_results = []
    for s_user in users:
        is_following = False
        if request.user.is_authenticated:
            is_following = Follow.objects.filter(follower=request.user, following=s_user).exists()
        
        search_results.append({
            'user_obj': s_user,
            'is_following': is_following
        })
        
    context = {
        'query': query,
        'search_results': search_results, 
    }
    return render(request, 'pirostagram/search.html', context)

#팔로우 토글
def toggle_follow(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(User, id=user_id)
        
        if target_user == request.user:
            return redirect('pirostagram:profile', username=target_user.username)
            
        follow_rel = Follow.objects.filter(follower=request.user, following=target_user)
        
        if follow_rel.exists():
            follow_rel.delete()  
        else:
            Follow.objects.create(follower=request.user, following=target_user)  
            
        return redirect('pirostagram:profile', username=target_user.username)
        
    return redirect('pirostagram:index')

# 게시글 
@login_required
def post_create(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if image:
            Post.objects.create(author=request.user, content=content, image=image)
            return redirect('pirostagram:index')
    return render(request, 'pirostagram/post_create.html')

# 좋아요 
@login_required
def post_like_toggle(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_exist = PostLike.objects.filter(post=post, user=request.user)
    if like_exist.exists():  #좋아요 취소
        like_exist.delete()
    else:
        PostLike.objects.create(post=post, user=request.user)
    return redirect(request.META.get('HTTP_REFERER', 'pirostagram:index'))

# 댓글 
@login_required
def comment_create(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
    return redirect(request.META.get('HTTP_REFERER', 'pirostagram:index'))


def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.author == request.user and request.method == 'POST':
        new_content = request.POST.get('content', '').strip()
        if new_content:
            comment.content = new_content
            comment.save()
            
    return redirect(request.META.get('HTTP_REFERER', 'pirostagram:index'))

def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER', 'pirostagram:index'))

# 게시글 수정
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'pirostagram/post_detail.html', {'post': post})

def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 작성자가 아닌 사람이 주소창으로 접근하면 차단
    if post.author != request.user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied 

    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        post.content = content
        if image:  # 이미지를 새로 업로드 했을 때만 변경
            post.image = image
        post.save()
        return redirect('pirostagram:index') 
    context = {
        'post': post,
    }
    return render(request, 'pirostagram/post_update.html', context)

# 게시글 삭제
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.author == request.user:  
        post.delete()
        
    return redirect('pirostagram:profile', username=request.user.username)

# 스토리
@login_required
def story_create(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        
        if image:
            Story.objects.create(author=request.user, image=image)
            return redirect('pirostagram:index')
            
    return render(request, 'pirostagram/story_create.html')