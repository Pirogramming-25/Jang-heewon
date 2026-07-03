from django.shortcuts import render, get_object_or_404, redirect
from .models import Idea, IdeaStar
from .forms import IdeaForm
from django.http import JsonResponse
from django.db.models import Count

# Create your views here.

def idea_list(request):
    sort_by = request.GET.get('sort', 'latest')
    queryset = Idea.objects.annotate(star_count= Count('stars'))
    
    if sort_by == 'stars':
        ideas = queryset.order_by('-star_count', '-id')     
    elif sort_by == 'name':
        ideas = queryset.order_by('title')                
    elif sort_by == 'oldest':
        ideas = queryset.order_by('created_at')           
    else: 
        ideas = queryset.order_by('-created_at')            
        
    current_user = request.user
    if not current_user.is_authenticated:
        current_user = User.objects.filter(username='testuser').first()

    user_starred_ids = []
    if current_user:
        user_starred_ids = IdeaStar.objects.filter(user=current_user).values_list('idea_id', flat=True)

    context = {
        'ideas': ideas,
        'sort_by': sort_by,
        'user_starred_ids': user_starred_ids,
    }
    return render(request, 'ideas/list.html', context)

def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST,request.FILES)
        if form.is_valid():
            idea = form.save()
            return redirect('idea_detail', pk=idea.pk)
    else:
            form = IdeaForm()
    return render(request, 'ideas/form.html', {'form': form, 'action': '등록'})

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    starred = False
    if request.user.is_authenticated:
        starred = IdeaStar.objects.filter(user=request.user, idea=idea).exists()
    
    context = {
        'idea': idea,
        'starred': starred,
    }
    return render(request, 'ideas/detail.html', context)

def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            idea = form.save()
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)
    return render(request, 'ideas/form.html', {'form': form, 'action': '수정', 'idea': idea})

def idea_delete(request, pk):
    if request.method == 'POST':
        idea = get_object_or_404(Idea, pk=pk)
        idea.delete()
    return redirect('idea_list')

def idea_interest_change(request, pk):
    if request.method == 'POST':
        idea = get_object_or_404(Idea, pk=pk)
        action = request.POST.get('action')
        
        if action == 'increase':
            idea.interest += 1
        elif action == 'decrease' and idea.interest > 0:
            idea.interest -= 1
            
        idea.save()
        return JsonResponse({'success': True, 'new_interest': idea.interest})
    return JsonResponse({'success': False}, status=400)

from django.contrib.auth.models import User

def idea_star_toggle(request, pk):
    if request.method == 'POST':
        idea = get_object_or_404(Idea, pk=pk)
        
        current_user = request.user
        if not current_user.is_authenticated:
            current_user = User.objects.first() or User.objects.create_user(username='testuser')
        
        star_filter = IdeaStar.objects.filter(user=current_user, idea=idea)
        
        if star_filter.exists():
            star_filter.delete()
            is_starred = False
        else:
            IdeaStar.objects.create(user=current_user, idea=idea)
            is_starred = True
        return JsonResponse({'success': True, 'is_starred': is_starred})
    return JsonResponse({'success': False}, status=400)