# Generated by Django 5.1 on 2024-10-21 05:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry_management', '0010_rename_image_feedback_images_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='images',
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='videos',
        ),
        migrations.AlterField(
            model_name='feedback',
            name='comments',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='patient_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='rating',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='FeedbackMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_file', models.FileField(upload_to='feedback_media/')),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], max_length=5)),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='enquiry_management.feedback')),
            ],
        ),
    ]
