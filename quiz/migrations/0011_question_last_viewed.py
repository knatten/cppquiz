# Generated by Django 1.11.4 on 2018-03-15 20:35


from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_auto_20180308_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='last_viewed',
            field=models.DateTimeField(default=timezone.now),
        ),
    ]
