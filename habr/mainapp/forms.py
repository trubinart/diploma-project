from django import forms

from mainapp.models import Article


class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('article_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = f'form-control {field_name}'
