# Generated by Django 3.0.3 on 2020-04-21 20:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("taggit", "0003_taggeditem_add_unique_index"),
        ("utils", "0003_auto_20170521_1932"),
    ]

    operations = [
        migrations.CreateModel(
            name="UUIDTaggedItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "object_id",
                    models.UUIDField(db_index=True, verbose_name="Object id"),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="utils_uuidtaggeditem_tagged_items",
                        to="contenttypes.ContentType",
                        verbose_name="Content type",
                    ),
                ),
                (
                    "tag",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="utils_uuidtaggeditem_items",
                        to="taggit.Tag",
                    ),
                ),
            ],
            options={"verbose_name": "Tag", "verbose_name_plural": "Tags",},
        ),
    ]
