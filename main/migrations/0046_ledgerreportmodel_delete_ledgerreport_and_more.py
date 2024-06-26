# Generated by Django 5.0.4 on 2024-05-31 14:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0045_alter_amountmodel_datetime_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LedgerReportModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=100, null=True)),
                ('DateTime', models.DateTimeField(default=datetime.datetime(2024, 5, 31, 20, 29, 5, 21061))),
                ('PartyName', models.CharField(blank=True, max_length=100, null=True)),
                ('Type', models.CharField(blank=True, max_length=100, null=True)),
                ('BiilNo', models.CharField(blank=True, max_length=100, null=True)),
                ('Debited', models.CharField(blank=True, default='0', max_length=100, null=True)),
                ('Cedited', models.CharField(blank=True, default='0', max_length=100, null=True)),
                ('Balance', models.CharField(blank=True, default='0', max_length=100, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='LedgerReport',
        ),
        migrations.AlterField(
            model_name='amountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 20, 29, 5, 18062)),
        ),
        migrations.AlterField(
            model_name='expanseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 20, 29, 5, 14061)),
        ),
        migrations.AlterField(
            model_name='purchaseentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 20, 29, 5, 61)),
        ),
        migrations.AlterField(
            model_name='salesentrymodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 20, 29, 5, 10062)),
        ),
        migrations.AlterField(
            model_name='useramountmodel',
            name='DateTime',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 31, 20, 29, 5, 20063)),
        ),
    ]
