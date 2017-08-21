from django import forms
from django.contrib.auth import get_user_model, authenticate

PickyUser = get_user_model()


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # label_suffix 값만 재정의(오버라이드) 한다. ":" 삭제
        kwargs.setdefault('label_suffix', '  ')
        # super는 상속받으면서 오버라이드할때 나머지 부모속성을 다시 호출(그대로 사용)
        super().__init__(*args, **kwargs)

    email = forms.CharField(
        max_length=30,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'email',
                'class': 'form-control',
                }
            )
        )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'password',
                'class': 'form-control',
                }
            )
        )

    def clean(self):
        # clean()메서드를 실행한 기본결과 dict를 가져옴
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        # username, password를 이용해 사용자 authenticate
        user = authenticate(
            email=email,
            password=password,
            )
        # 인증에 성공할 경우, Form의 cleaned_data의 'user'
        # 키에 인증된 User객체를 할당
        if user is not None:
            self.cleaned_data['user'] = user
        # 인증에 실패한 경우, is_valid()를 통과하지 못하도록
        # ValidationError를 발생시킴
        else:
            raise forms.ValidationError(
                'Login failed.'
                )
        return self.cleaned_data
