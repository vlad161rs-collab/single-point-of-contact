# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregistrationrequest',
            name='password_hash',
            field=models.CharField(blank=True, max_length=128, verbose_name='Хеш пароля'),
        ),
    ]





