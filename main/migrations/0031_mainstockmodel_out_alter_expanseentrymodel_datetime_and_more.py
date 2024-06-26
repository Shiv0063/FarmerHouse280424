# Generated by Django 5.0.4 on 2024-05-14 14:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_alter_expanseentrymodel_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainstockmodel',
            name='out',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='expanseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 14, 20, 3, 25, 347178)),
        ),
        migrations.AlterField(
            model_name='purchaseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 14, 20, 3, 25, 347178)),
        ),
        migrations.AlterField(
            model_name='salesentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 14, 20, 3, 25, 347178)),
        ),
    ]
