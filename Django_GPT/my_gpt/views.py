from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
import json
from .forms import AnalysisForm
from .models import InferenceHistory
from .decorators import login_required_with_alert
from .services.sentiment import analyze_twitter_sentiment
from .services.summarizer import summarize_text
from .services.moderator import analyze_toxicity
from .services.combo import process_combo

def handle_analysis_request(request, template_name, page_info, min_len, max_len, ai_service_func, task_type, is_login_required=False):
    if is_login_required and not request.user.is_authenticated:
        return redirect(f"/accounts/login/?next={request.path}&required=1")

    if request.method == 'POST':
        form = AnalysisForm(request.POST, min_length=min_len, max_length=max_len)
        
        if not form.is_valid():
            errors = [error for field_errors in form.errors.values() for error in field_errors]
            return JsonResponse({'success': False, 'error': errors[0]}, status=400)
        
        user_text = form.cleaned_data['content']

        try:
            result = ai_service_func(user_text)

            current_user = request.user if request.user.is_authenticated else None

            InferenceHistory.objects.create(
                user=current_user,
                task=task_type,
                input_text=user_text,
                output_text=result
            )

            filter_kwargs = {'task': task_type}
            if request.user.is_authenticated:
                filter_kwargs['user'] = request.user
            else:
                filter_kwargs['user__isnull'] = True

            recent_logs = list(
                InferenceHistory.objects.filter(**filter_kwargs)
                .order_by('-created_at')[:5]
                .values('input_text', 'output_text', 'created_at')
            )

            return JsonResponse({
                'success': True,
                'result': result,
                'recent_logs': recent_logs
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': f"처리 중 오류가 발생했습니다: {str(e)}"}, status=500)

    filter_kwargs = {'task': task_type}
    if request.user.is_authenticated:
        filter_kwargs['user'] = request.user
    else:
        filter_kwargs['user__isnull'] = True

    recent_logs = InferenceHistory.objects.filter(**filter_kwargs).order_by('-created_at')[:5]

    context = {
        'page_info': page_info,
        'recent_logs': recent_logs,
        'min_length': min_len,
        'max_length': max_len,
    }
    return render(request, template_name, context)

def sentiment_view(request):
    page_info = {
        'title': '감정 분석',
        'model_name': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
        'language': '영어 (English)'
    }
    return handle_analysis_request(
        request, 
        'my_gpt/sentiment.html', 
        page_info, 
        min_len=1, 
        max_len=1000, 
        ai_service_func=analyze_twitter_sentiment,
        task_type=InferenceHistory.Task.SENTIMENT,
        is_login_required=False
    )

@login_required_with_alert
def summarize_view(request):
    page_info = {
        'title': '문서 요약',
        'model_name': 'sshleifer/distilbart-cnn-6-6',
        'language': '영어 (English)'
    }
    return handle_analysis_request(
        request, 
        'my_gpt/summarize.html', 
        page_info, 
        min_len=100,
        max_len=5000,
        ai_service_func=summarize_text,
        task_type=InferenceHistory.Task.SUMMARIZE,
        is_login_required=True
    )

@login_required_with_alert
def moderate_view(request):
    page_info = {
        'title': '유해 표현 분석',
        'model_name': 'unitary/toxic-bert',
        'language': '영어 (English)'
    }
    return handle_analysis_request(
        request, 
        'my_gpt/moderate.html', 
        page_info, 
        min_len=1,
        max_len=1000,
        ai_service_func=analyze_toxicity,
        task_type=InferenceHistory.Task.MODERATE,
        is_login_required=True
    )

@login_required_with_alert
def combo_view(request):
    task_type = getattr(InferenceHistory.Task, 'COMBO', 'COMBO')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_text = data.get('text', '').strip()

            if not user_text:
                return JsonResponse({'success': False, 'error': '분석할 텍스트를 입력해 주세요.'}, status=400)

            combo_result = process_combo(user_text)

            if request.user.is_authenticated:
                InferenceHistory.objects.create(
                    user=request.user,
                    task=task_type,
                    input_text=user_text,
                    output_text=json.dumps(combo_result, ensure_ascii=False)
                )

            filter_kwargs = {'task': task_type}
            if request.user.is_authenticated:
                filter_kwargs['user'] = request.user
            else:
                filter_kwargs['user__isnull'] = True

            recent_logs = list(
                InferenceHistory.objects.filter(**filter_kwargs)
                .order_by('-created_at')[:5]
                .values('input_text', 'output_text', 'created_at')
            )

            return JsonResponse({
                'success': True,
                'result': combo_result,
                'recent_logs': recent_logs
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': f"분석 처리 중 오류 발생: {str(e)}"}, status=500)

    filter_kwargs = {'task': task_type}
    if request.user.is_authenticated:
        filter_kwargs['user'] = request.user
    else:
        filter_kwargs['user__isnull'] = True

    recent_logs = InferenceHistory.objects.filter(**filter_kwargs).order_by('-created_at')[:5]

    context = {
        'page_info': {
            'title': '복합 분석 (Combo)',
            'model_name': 'RoBERTa / DistilBART / Toxic-BERT',
            'language': '영어 (English)'
        },
        'recent_logs': recent_logs,
        'min_length': 200,
        'max_length': 5000,
    }
    return render(request, 'my_gpt/combo.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/sentiment/')
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')