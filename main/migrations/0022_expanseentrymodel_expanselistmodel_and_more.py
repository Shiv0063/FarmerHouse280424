# Generated by Django 5.0.4 on 2024-05-05 10:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_purchaseentrymodel_date_salesentrymodel_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpanseEntryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=100, null=True)),
                ('TypeofPayment', models.CharField(blank=True, max_length=100, null=True)),
                ('DateTime', models.DateTimeField(default=datetime.datetime(2024, 5, 5, 15, 53, 14, 308250))),
                ('PartyName', models.CharField(blank=True, max_length=100, null=True)),
                ('ProductId', models.CharField(blank=True, max_length=100, null=True)),
                ('Amount', models.CharField(blank=True, max_length=100, null=True)),
                ('Date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExpanseListModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductId', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.CharField(blank=True, max_length=100, null=True)),
                ('Expanse', models.CharField(blank=True, max_length=100, null=True)),
                ('Amount', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='purchaseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 15, 53, 14, 308250)),
        ),
        migrations.AlterField(
            model_name='salesentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 15, 53, 14, 308250)),
        ),
    ]
