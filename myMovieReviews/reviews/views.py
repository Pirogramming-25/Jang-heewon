from django.shortcuts import render, get_object_or_404, redirect
from .models import Review


# Create your views here.

def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.hours = review.time // 60
    review.minutes = review.time % 60
    return render(request, 'reviews/review_detail.html', {'review': review})

def review_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        director = request.POST.get('director')
        actor = request.POST.get('actor')
        genre = request.POST.get('genre')
        star = request.POST.get('star')
        time = request.POST.get('time')
        content = request.POST.get('content')

        review = Review.objects.create(
            title=title,
            director=director,
            actor=actor,
            genre=genre,
            star=star,
            time=time,
            content=content
        )
        return redirect('review-list')
    return render(request, 'reviews/review_form.html')

def review_update(request,pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.director = request.POST.get('director')
        review.actor = request.POST.get('actor')
        review.genre = request.POST.get('genre')
        review.star = request.POST.get('star')
        review.time = request.POST.get('time')
        review.content = request.POST.get('content')
        review.save()
        return redirect('review-detail', pk=review.pk)
    return render(request, 'reviews/review_form.html', {'review': review})

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review-list')
    return render(request, 'reviews/review_delete.html', {'review': review})

def review_list(request):
    sort_param = request.GET.get('sort', 'latest')
    
    if sort_param == 'title':
        order = 'title'          
    elif sort_param == 'star':
        order = '-star'          
    elif sort_param == 'time':
        order = '-time'         
    else:
        order = '-created_at'   

    reviews = Review.objects.all().order_by(order)
        
    return render(request, 'reviews/review_list.html', {'reviews': reviews})