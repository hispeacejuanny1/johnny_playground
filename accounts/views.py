#accounts/views.py

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 관리자 승인 전까지 비활성화!
            user.save()
            print(f"새 사용자 생성: {user.username}, is_active: {user.is_active}")  # 디버그
            return render(request, 'registration/signup_done.html')  # 가입완료 안내
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'
    
    def form_invalid(self, form):
        print(f"로그인 실패: {form.errors}")  # 디버그
        print(f"Non-field errors: {form.non_field_errors}")  # 디버그
        return super().form_invalid(form)