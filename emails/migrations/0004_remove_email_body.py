# Generated by Django 5.0 on 2024-12-08 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0003_alter_email_attachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='body',
        ),
    ]