from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import UserProfile, UserRegistrationRequest, Department


class UserRegistrationRequestForm(forms.ModelForm):
    """Форма запроса на регистрацию"""
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Минимум 8 символов'
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserRegistrationRequest
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 
                  'department', 'position', 'requested_role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'requested_role': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        departments = Department.objects.all().order_by('name')
        self.fields['department'].queryset = departments
        self.fields['department'].widget.attrs.update({'class': 'form-control'})
        if departments.exists():
            self.fields['department'].empty_label = 'Выберите отдел (необязательно)'
        else:
            self.fields['department'].empty_label = 'Нет доступных отделов'
        self.fields['department'].required = False
        self.fields['department'].widget.attrs['style'] = 'width: 100%;'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password_hash = self.cleaned_data['password1']  # Сохраняем для создания пользователя после одобрения
        if commit:
            instance.save()
        return instance


class UserProfileForm(forms.ModelForm):
    """Форма редактирования профиля пользователя"""
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Фамилия'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Email'
    )

    class Meta:
        model = UserProfile
        fields = ['phone', 'department', 'position']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
        departments = Department.objects.all().order_by('name')
        self.fields['department'].queryset = departments
        self.fields['department'].widget.attrs.update({'class': 'form-control'})
        if departments.exists():
            self.fields['department'].empty_label = 'Выберите отдел (необязательно)'
        else:
            self.fields['department'].empty_label = 'Нет доступных отделов'
        self.fields['department'].required = False
        self.fields['department'].widget.attrs['style'] = 'width: 100%;'

    def save(self, user=None, commit=True):
        instance = super().save(commit=False)
        if user:
            user.first_name = self.cleaned_data.get('first_name', '')
            user.last_name = self.cleaned_data.get('last_name', '')
            user.email = self.cleaned_data.get('email', '')
            user.save()
        department = self.cleaned_data.get('department')
        if department:
            instance.department = department
        else:
            instance.department = None
        if commit:
            instance.save()
        return instance


class PasswordChangeCustomForm(PasswordChangeForm):
    """Кастомная форма смены пароля"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

