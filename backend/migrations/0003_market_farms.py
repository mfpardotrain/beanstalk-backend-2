# Generated by Django 4.1.2 on 2022-11-05 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_farmvegetableorder_farmer_marketinfo_farmer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='farms',
            field=models.ManyToManyField(blank=True, to='backend.farm'),
        ),
    ]
