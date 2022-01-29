from django import forms

from mainapp.models import Article, ArticleComment


class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('likes',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['categories'].label = 'Выберете категорию'
        self.fields['title'].label = 'Укажите заголовок статьи'
        self.fields['subtitle'].label = 'Укажите краткое описание статьи'
        self.fields['main_img'].label = 'Загрузите картинку к статье'
        self.fields['text'].label = 'Напишите статью'
        self.fields['categories'].widget.attrs['value'] = 'Укажите раздел'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'


class CreationCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ('article_comment', 'text', 'user')

    def __init__(self, *args, **kwargs):
        super(CreationCommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = 'Напишите свой комментарий'
        self.fields['text'].widget.attrs['name'] = 'text'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            self.fields['text'].widget.attrs['class'] = 'comment_input'
