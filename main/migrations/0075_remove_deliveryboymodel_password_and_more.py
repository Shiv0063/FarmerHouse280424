# Generated by Django 5.0.4 on 2024-06-12 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0074_alter_amountmodel_datetime_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryboymodel',
            name='PassWord',
        ),
        migrations.AlterField(
            model_name='amountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 12, 18, 4, 10, 815867)),
        ),
        migrations.AlterField(
            model_name='expanseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 12, 18, 4, 10, 809975)),
        ),
        migrations.AlterField(
            model_name='purchaseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 12, 18, 4, 10, 794087)),
        ),
        migrations.AlterField(
            model_name='salesentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 12, 18, 4, 10, 804868)),
        ),
        migrations.AlterField(
            model_name='useramountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 12, 18, 4, 10, 817867)),
        ),
    ]
