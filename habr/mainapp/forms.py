from datetime import date, timedelta

from django import forms

from mainapp.models import Article, ArticleComment
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from authapp.models import UserProfile, User
from mainapp.models import ArticleComment


class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('article_number',)

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

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'ivanov2019'
        self.fields['email'].widget.attrs['placeholder'] = 'ivanov2019@gmail.com'
        self.fields['password'].widget.attrs['placeholder'] = ' • • • • • • • • • •'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['class'] = 'form-input'

# ====
# class UserProfileForm(forms.ModelForm):
class UserProfileForm(UserCreationForm):
    # class UserProfileEditForm(UserChangeForm):
    """Чтение и изменение объекта пользователя"""

    class Meta:
        model = UserProfile
        # fields = ('name', 'birthday', 'bio', 'avatar')
        fields = '__all__'
        # exclude = ('user',)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.help_text = ''
    #         if field_name == 'password':
    #             field.widget = forms.HiddenInput()
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # self.fields['user'].widget = forms.HiddenInput()
        self.fields['name'].widget.attrs['placeholder'] = 'Имя Фамилия'
        self.fields['name'].widget.attrs['type'] = 'text'
        self.fields['name'].widget.attrs['name'] = 'name'
        self.fields['birthday'].widget.attrs['name'] = 'birthday'
        self.fields['birthday'].widget = forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})
        # self.fields['bio'].widget.attrs['type'] = 'textarea'
        self.fields['bio'].widget = forms.Textarea(attrs={'rows': 3, 'cols:': 60})
        self.fields['bio'].widget.attrs['name'] = 'bio'
        self.fields['bio'].widget.attrs['placeholder'] = 'Краткое описание'
        self.fields['avatar'].widget.attrs['name'] = 'avatar'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['class'] = 'inputFild'
            # if field_name == 'password':
            #     field.widget = forms.HiddenInput()
            # self.fields['text'].widget.attrs['class'] = 'comment_input'

    # def clean_birthday(self):
    #     data = self.cleaned_data['birthday']
    #     # return_date = datetime.date.today() + datetime.timedelta(days=5)
    #     # 2555 - 7 лет
    #     dates = date.today() - timedelta(days=2555)
    #     if data < dates:
    #         raise forms.ValidationError("Вы слишком молоды!")
    #     return data


# class UserProfileForm(forms.ModelForm):
class UserProfileEditForm(forms.ModelForm):
    """Чтение и изменение объекта пользователя"""

    class Meta:
        model = UserProfile
        # fields = ('name', 'birthday', 'bio')
        fields = ('name', 'birthday', 'bio', 'avatar')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.help_text = ''
    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Имя Фамилия'
        self.fields['name'].widget.attrs['type'] = 'text'
        self.fields['name'].widget.attrs['name'] = 'name'
        self.fields['birthday'].widget.attrs['name'] = 'birthday'
        self.fields['birthday'].widget = forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})
        # self.fields['bio'].widget.attrs['type'] = 'textarea'
        self.fields['bio'].widget = forms.Textarea(attrs={'rows': 3, 'cols:': 60})
        self.fields['bio'].widget.attrs['name'] = 'bio'
        self.fields['bio'].widget.attrs['placeholder'] = 'Краткое описание'
        self.fields['avatar'].widget.attrs['name'] = 'avatar'

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['class'] = 'inputFild'
            # if field_name == 'password':
            #     field.widget = forms.HiddenInput()
            # self.fields['text'].widget.attrs['class'] = 'comment_input'

    def clean_birthday(self):
        data = self.cleaned_data['birthday']
        # return_date = datetime.date.today() + datetime.timedelta(days=5)
        # 2555 - 7 лет
        dates = date.today() - timedelta(days=2555)
        if data < dates:
            raise forms.ValidationError("Вы слишком молоды!")
        return data
