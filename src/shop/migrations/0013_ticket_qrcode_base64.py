# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-25 16:58


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("shop", "0012_ticket")]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="qrcode_base64",
            field=models.TextField(blank=True, null=True),
        )
    ]
