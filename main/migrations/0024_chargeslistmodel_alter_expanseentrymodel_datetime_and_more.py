# Generated by Django 5.0.4 on 2024-05-08 06:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_chargesmodel_alter_expanseentrymodel_datetime_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChargesListModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=100, null=True)),
                ('Charges', models.CharField(blank=True, max_length=100, null=True)),
                ('ProductId', models.CharField(blank=True, max_length=100, null=True)),
                ('Amount', models.CharField(blank=True, max_length=100, null=True)),
                ('Tax', models.CharField(blank=True, max_length=100, null=True)),
                ('TotalAmount', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='expanseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 8, 11, 39, 28, 791806)),
        ),
        migrations.AlterField(
            model_name='purchaseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 8, 11, 39, 28, 776057)),
        ),
        migrations.AlterField(
            model_name='salesentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 8, 11, 39, 28, 791806)),
        ),
    ]
