# Generated by Django 5.0.4 on 2024-05-31 15:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0048_salesentrymodel_status_alter_amountmodel_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseentrymodel',
            name='status',
            field=models.CharField(blank=True, default='0', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='amountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 21, 22, 26, 749437)),
        ),
        migrations.AlterField(
            model_name='expanseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 21, 22, 26, 744437)),
        ),
        migrations.AlterField(
            model_name='ledgerreportmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 21, 22, 26, 751437)),
        ),
        migrations.AlterField(
            model_name='purchaseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 21, 22, 26, 731438)),
        ),
        migrations.AlterField(
            model_name='salesentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 21, 22, 26, 741437)),
        ),
        migrations.AlterField(
            model_name='useramountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 21, 22, 26, 750437)),
        ),
    ]