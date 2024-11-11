# Generated by Django 5.1 on 2024-10-20 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquiry_management', '0007_delete_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=100)),
                ('rating', models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])),
                ('review_text', models.TextField(blank=True, null=True)),
                ('review_image', models.ImageField(blank=True, null=True, upload_to='review_images/')),
                ('review_video', models.FileField(blank=True, null=True, upload_to='review_videos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
