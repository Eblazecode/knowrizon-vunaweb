# Generated by Django 5.1 on 2024-09-07 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('knowrizonApp', '0002_students'),
    ]

    operations = [
        migrations.RenameField(
            model_name='students',
            old_name='students_gender',
            new_name='student_gender',
        ),
    ]
