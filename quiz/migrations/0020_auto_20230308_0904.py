# Generated by Django 3.2 on 2023-03-08 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0019_auto_20210322_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='questioninquiz',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='usersanswer',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
