# Generated by Django 5.0.4 on 2024-06-08 14:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0066_salesentrymodel_orderno_alter_amountmodel_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 8, 20, 28, 44, 986311)),
        ),
        migrations.AlterField(
            model_name='expanseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 8, 20, 28, 44, 986311)),
        ),
        migrations.AlterField(
            model_name='ledgerreportmodel',
            name='LRDate',
            field=models.DateField(default=datetime.date(2024, 6, 8)),
        ),
        migrations.AlterField(
            model_name='purchaseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 8, 20, 28, 44, 970604)),
        ),
        migrations.AlterField(
            model_name='salesentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 8, 20, 28, 44, 986311)),
        ),
        migrations.AlterField(
            model_name='useramountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 8, 20, 28, 45, 1885)),
        ),
    ]