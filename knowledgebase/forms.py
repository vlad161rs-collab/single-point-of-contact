from django import forms
from .models import Article, Request, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'video', 'audio']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['content'].required = True


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Status should not be editable by regular users in the form
        # It should be managed through admin or special views
        self.fields['title'].required = True
        self.fields['description'].required = True


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите ваш комментарий...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].required = True
        self.fields['text'].label = 'Комментарий'
    
    def _post_clean(self):
        """Переопределяем пост-валидацию, чтобы не вызывать clean() модели до установки article/request"""
        # Вызываем construct_instance для установки значений полей формы в instance
        # Но НЕ вызываем self.instance.full_clean(), 
        # так как article/request будут установлены после form.save(commit=False)
        from django.forms.models import construct_instance
        
        opts = self._meta
        exclude = self._get_validation_exclusions()
        
        # Foreign Keys being used to represent inline relationships
        from django.forms.models import InlineForeignKeyField
        for name, field in self.fields.items():
            if isinstance(field, InlineForeignKeyField):
                exclude.add(name)
        
        try:
            self.instance = construct_instance(
                self, self.instance, opts.fields, opts.exclude
            )
        except forms.ValidationError as e:
            self._update_errors(e)
        
        # НЕ вызываем self.instance.full_clean(exclude=exclude)
        # Валидация модели будет вызвана вручную в views после установки article/request
