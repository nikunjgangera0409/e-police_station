# Generated by Django 3.2 on 2021-04-16 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ep_app', '0006_complain'),
    ]

    operations = [
        migrations.CreateModel(
            name='Police_Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Police_station_name', models.CharField(max_length=200)),
                ('address', models.TextField(max_length=200)),
                ('phone_no', models.CharField(max_length=200)),
            ],
        ),
    ]