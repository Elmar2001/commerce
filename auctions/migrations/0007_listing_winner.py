# Generated by Django 3.1 on 2020-09-20 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200915_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.CharField(default=None, max_length=128),
            preserve_default=False,
        ),
    ]
