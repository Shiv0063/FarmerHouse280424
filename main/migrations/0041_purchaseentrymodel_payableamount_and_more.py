# Generated by Django 5.0.4 on 2024-05-31 07:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_partymodel_cedited_partymodel_debited_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseentrymodel',
            name='PayableAmount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='salesstockmodel',
            name='PayableAmount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='amountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 12, 57, 52, 87058)),
        ),
        migrations.AlterField(
            model_name='expanseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 12, 57, 52, 87058)),
        ),
        migrations.AlterField(
            model_name='purchaseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 12, 57, 52, 67060)),
        ),
        migrations.AlterField(
            model_name='salesentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 12, 57, 52, 77062)),
        ),
        migrations.AlterField(
            model_name='useramountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 12, 57, 52, 87058)),
        ),
    ]
