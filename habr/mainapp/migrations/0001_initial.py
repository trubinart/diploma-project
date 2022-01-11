# Generated by Django 4.0 on 2022-01-11 11:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='name_categories')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
            ],
        ),
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Create Date')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.basemodel')),
                ('num_article', models.PositiveIntegerField(unique=True)),
                ('title', models.CharField(max_length=60)),
                ('subtitle', models.CharField(max_length=100)),
                ('main_img', models.ImageField(upload_to='article_images')),
                ('text', models.TextField(max_length=300, verbose_name='Text Article')),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.articlecategories')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='article_author', to='authapp.user', verbose_name='Author article')),
            ],
            options={
                'db_table': 'article',
                'ordering': ['-created_timestamp'],
            },
            bases=('mainapp.basemodel',),
        ),
        migrations.CreateModel(
            name='ArticleLike',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.basemodel')),
                ('like', models.BooleanField(verbose_name='Like')),
                ('article_like', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='article_like', to='mainapp.article', verbose_name='Article for like')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='like_author', to='authapp.user', verbose_name='Like Author')),
            ],
            options={
                'db_table': 'article_likes',
                'ordering': ['-created_timestamp'],
            },
            bases=('mainapp.basemodel',),
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='mainapp.basemodel')),
                ('text', models.TextField(max_length=300, verbose_name='Comment text')),
                ('article_comment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='article_comment', to='mainapp.article', verbose_name='Article for comment')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='comment_author', to='authapp.user', verbose_name='Comment Author')),
            ],
            options={
                'db_table': 'article_comments',
                'ordering': ['-created_timestamp'],
            },
            bases=('mainapp.basemodel',),
        ),
    ]
