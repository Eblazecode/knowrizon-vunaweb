from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('knowrizonApp', '0017_pdf_materials_pdf_material_ref_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal_materials',
            fields=[
                ('journal_material_id', models.AutoField(primary_key=True)),
                ('journal_material_title', models.CharField(max_length=50)),
                ('journal_material_author', models.CharField(max_length=50)),
                ('journal_material_category', models.CharField(max_length=50)),
                ('journal_upload_date', models.CharField(max_length=50)),
                ('journal_material_tags', models.CharField(max_length=50)),
                ('journal_for_department', models.CharField(max_length=50)),
                ('journal_for_faculty', models.CharField(max_length=50)),
                ('journal_for_level', models.CharField(max_length=50)),
                ('journal_material_description', models.CharField(max_length=555, default='ABSTRACT NOT AVAILABLE')),
                ('journal_material_file', models.FileField(upload_to='materials/journals/', blank=True, null=True)),
                ('journal_material_cover_image', models.ImageField(upload_to='materials/journals/cover/', blank=True, null=True)),
                ('journal_material_created_at', models.DateTimeField(auto_now_add=True)),
                ('journal_material_updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),

    ]