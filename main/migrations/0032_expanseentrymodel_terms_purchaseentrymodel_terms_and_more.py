# Generated by Django 5.0.4 on 2024-05-17 08:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_mainstockmodel_out_alter_expanseentrymodel_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expanseentrymodel',
            name='Terms',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='purchaseentrymodel',
            name='Terms',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='salesentrymodel',
            name='Terms',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='expanseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 17, 14, 28, 43, 372174)),
        ),
        migrations.AlterField(
            model_name='purchaseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 17, 14, 28, 43, 362174)),
        ),
        migrations.AlterField(
            model_name='salesentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 17, 14, 28, 43, 362174)),
        ),
    ]