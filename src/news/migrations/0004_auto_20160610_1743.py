# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-10 17:43


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_newsitem_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsitem',
            name='slug',
            field=models.SlugField(max_length=255),
        ),
    ]