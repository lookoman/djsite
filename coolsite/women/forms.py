from django import forms
from django.core.exceptions import ValidationError

from .models import *


class AddPostForm2(forms.Form):
    title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))
    slug = forms.SlugField(max_length=255, label="URL")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Статья")
    is_published = forms.BooleanField(label="Опубликовать", required=False, initial=True)
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(), label="Категория", empty_label="Категория не выбрана",
        required=False
    )


class AddPostForm(forms.ModelForm):
    def __int__(self, *args, **kwargs):
        super(AddPostForm, self).__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "asdf"

    class Meta:
        model = Women
        # fields = '__all__'
        # exclude = ('photo',)
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return title
