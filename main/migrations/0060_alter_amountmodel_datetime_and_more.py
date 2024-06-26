# Generated by Django 5.0.4 on 2024-06-02 12:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0059_alter_amountmodel_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 2, 17, 42, 22, 964612)),
        ),
        migrations.AlterField(
            model_name='expanseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 2, 17, 42, 22, 959612)),
        ),
        migrations.AlterField(
            model_name='purchaseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 2, 17, 42, 22, 946614)),
        ),
        migrations.AlterField(
            model_name='salesentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 2, 17, 42, 22, 956612)),
        ),
        migrations.AlterField(
            model_name='useramountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 2, 17, 42, 22, 966612)),
        ),
    ]
