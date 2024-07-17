# Generated by Django 5.0.4 on 2024-06-12 14:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0076_salesentrymodel_deliveryboyno_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesentrymodel',
            name='BillClear',
            field=models.CharField(blank=True, default='0', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='amountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 12, 19, 42, 54, 719946)),
        ),
        migrations.AlterField(
            model_name='expanseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 12, 19, 42, 54, 719946)),
        ),
        migrations.AlterField(
            model_name='purchaseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 12, 19, 42, 54, 704323)),
        ),
        migrations.AlterField(
            model_name='salesentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 12, 19, 42, 54, 719946)),
        ),
        migrations.AlterField(
            model_name='useramountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 12, 19, 42, 54, 719946)),
        ),
    ]
