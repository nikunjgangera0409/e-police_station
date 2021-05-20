# Generated by Django 3.2 on 2021-05-06 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ep_app', '0017_auto_20210506_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='police_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ep_app.police_station'),
        ),
        migrations.AddField(
            model_name='fir',
            name='police_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ep_app.police_station'),
        ),
    ]
