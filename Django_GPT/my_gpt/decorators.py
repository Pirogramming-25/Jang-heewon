from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages  # 추가

def login_required_with_alert(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # 리다이렉트 전 알림 메시지 등록
            messages.warning(request, "로그인이 필요한 서비스입니다.")
            
            login_url = reverse('login')
            current_path = request.path
            return redirect(f"{login_url}?next={current_path}")
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view