# Generated by Django 3.1 on 2020-09-12 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_category_comment_listing_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(max_length=128),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
