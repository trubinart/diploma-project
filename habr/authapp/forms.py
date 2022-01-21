from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from authapp.models import User, UserProfile


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'ivanov2019'
        self.fields['email'].widget.attrs['placeholder'] = 'ivanov2019@gmail.com'
        self.fields['password1'].widget.attrs['placeholder'] = ' • • • • • • • • • •'
        self.fields['password2'].widget.attrs['placeholder'] = ' • • • • • • • • • •'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['class'] = 'form-input'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # fields = ('name', 'birthday', 'bio', 'avatar')
        fields = ('name', 'birthday', 'bio')
        # # 'name': forms.TextInput(attrs={'class': 'inputFild', 'placeholder': 'Имя Фамилия'}),
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'inputFild', 'placeholder': 'Имя Фамилия'}),
        #     'birthday': forms.DateInput(attrs={'class': 'inputFild'}),
        #     'bio': forms.Textarea(attrs={'class': 'inputFild', 'placeholder': 'Краткое описание'}),
        # }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'first_and_last_name'
        self.fields['name'].widget.attrs['type'] = 'text'
        # self.fields['name'].widget.attrs['name'] = 'fieldFirstName'
        self.fields['name'].widget.attrs['name'] = 'name'
        self.fields['birthday'].widget.attrs['placeholder'] = '19.01.2022'
        self.fields['birthday'].widget.attrs['type'] = 'date'
        self.fields['bio'].widget.attrs['placeholder'] = 'Краткое описание'
        self.fields['bio'].widget.attrs['type'] = 'textarea'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['class'] = 'inputFild'

# class UserProfileEditForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         # fields = ('name', 'birthday', 'bio', 'avatar')
#         fields = ('name', 'birthday', 'bio')
#         # # 'name': forms.TextInput(attrs={'class': 'inputFild', 'placeholder': 'Имя Фамилия'}),
#         # widgets = {
#         #     'name': forms.TextInput(attrs={'class': 'inputFild', 'placeholder': 'Имя Фамилия'}),
#         #     'birthday': forms.DateInput(attrs={'class': 'inputFild'}),
#         #     'bio': forms.Textarea(attrs={'class': 'inputFild', 'placeholder': 'Краткое описание'}),
#         # }
#
#     def __init__(self, *args, **kwargs):
#         super(UserProfileEditForm, self).__init__(*args, **kwargs)
#         # super().__init__(*args, **kwargs)
#         self.fields['name'].widget.attrs['placeholder'] = 'first_and_last_name'
#         self.fields['name'].widget.attrs['type'] = 'text'
#         # self.fields['name'].widget.attrs['name'] = 'fieldFirstName'
#         self.fields['name'].widget.attrs['name'] = 'name'
#         self.fields['birthday'].widget.attrs['placeholder'] = '19.01.2022'
#         self.fields['birthday'].widget.attrs['type'] = 'date'
#         self.fields['bio'].widget.attrs['placeholder'] = 'Краткое описание'
#         self.fields['bio'].widget.attrs['type'] = 'textarea'
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'form-control'
#             field.widget.attrs['class'] = 'inputFild'