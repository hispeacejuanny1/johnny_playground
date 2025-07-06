# accounts/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _("아이디 또는 비밀번호가 잘못되었습니다. (대소문자 구분)"),
        'inactive': _("계정이 비활성화되어 있습니다. 관리자 승인을 기다려주세요."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            try:
                # 사용자 존재 여부 확인 (is_active 상관없이)
                user = User.objects.get(username=username)
                
                # 비밀번호 확인
                if user.check_password(password):
                    self.user_cache = user
                    # 비활성 계정인지 확인
                    if not user.is_active:
                        raise forms.ValidationError(
                            self.error_messages['inactive'],
                            code='inactive',
                        )
                    # 활성 사용자라면 추가 검증
                    self.confirm_login_allowed(user)
                else:
                    # 비밀번호가 틀림
                    raise self.get_invalid_login_error()
                    
            except User.DoesNotExist:
                # 사용자가 존재하지 않음
                raise self.get_invalid_login_error()

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        # 추가적인 사용자 검증이 필요한 경우 여기에 구현
        pass