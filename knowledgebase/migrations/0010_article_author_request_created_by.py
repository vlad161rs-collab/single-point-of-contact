# Generated manually

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0009_alter_article_options_alter_comment_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='articles',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Автор'
            ),
        ),
        migrations.AddField(
            model_name='request',
            name='created_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='requests',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Создатель'
            ),
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['author'], name='knowledgeba_author_123456_idx'),
        ),
        migrations.AddIndex(
            model_name='request',
            index=models.Index(fields=['created_by'], name='knowledgeba_created_789abc_idx'),
        ),
    ]



