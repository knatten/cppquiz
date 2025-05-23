# Generated by Django 5.2 on 2025-05-12 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0025_question_auto_format'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='state',
            field=models.CharField(choices=[('NEW', 'New'), ('DRA', 'Draft'), ('WAI', 'Waiting'), ('ACC', 'Accepted'), ('SCH', 'Scheduled'), ('REF', 'Refused'), ('PUB', 'Published'), ('RET', 'Retracted')], default='NEW', max_length=3),
        ),
    ]
