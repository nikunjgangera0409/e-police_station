# Generated by Django 3.2 on 2021-05-05 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ep_app', '0007_police_station'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crime_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crime_category', models.CharField(max_length=256)),
            ],
        ),
    ]
