# Generated by Django 5.1.5 on 2025-01-30 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowrizonApp', '0019_academic_staff_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academic_staff',
            name='academic_staff_dept',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='academic_staff',
            name='academic_staff_email',
            field=models.EmailField(max_length=250),
        ),
        migrations.AlterField(
            model_name='academic_staff',
            name='academic_staff_fname',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='academic_staff',
            name='academic_staff_gender',
            field=models.CharField(default='Not specified', max_length=250),
        ),
        migrations.AlterField(
            model_name='academic_staff',
            name='academic_staff_lname',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='academic_staff',
            name='academic_staff_password',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='academic_staff',
            name='academic_staff_phone',
            field=models.CharField(default='', max_length=75),
        ),
        migrations.AlterField(
            model_name='academic_staff',
            name='academic_staff_position',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='journal_materials',
            name='journal_material_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
