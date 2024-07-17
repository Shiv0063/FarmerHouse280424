# Generated by Django 5.0.4 on 2024-07-01 11:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0081_alter_amountmodel_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesstockmodel',
            name='LossMargin',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='amountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 16, 36, 1, 239838)),
        ),
        migrations.AlterField(
            model_name='expanseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 16, 36, 1, 224216)),
        ),
        migrations.AlterField(
            model_name='purchaseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 16, 36, 1, 224216)),
        ),
        migrations.AlterField(
            model_name='salesentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 16, 36, 1, 224216)),
        ),
        migrations.AlterField(
            model_name='useramountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 16, 36, 1, 239838)),
        ),
    ]
