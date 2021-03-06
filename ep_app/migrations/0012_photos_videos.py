# Generated by Django 3.2 on 2021-05-05 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ep_app', '0011_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photos_Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Description', models.CharField(max_length=100, null=True)),
                ('Photo', models.ImageField(max_length=500, upload_to='photos_videos/')),
                ('Video', models.FileField(max_length=500, upload_to='photos_videos/')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
