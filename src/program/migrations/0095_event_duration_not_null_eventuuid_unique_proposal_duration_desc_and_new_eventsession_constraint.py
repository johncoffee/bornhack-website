# Generated by Django 3.0.3 on 2020-06-21 23:56

import uuid

import django.contrib.postgres.constraints
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("program", "0094_tags_blank"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="duration_minutes",
            field=models.PositiveIntegerField(
                blank=True,
                default=None,
                help_text="The duration of this event in minutes. Leave blank to use the default from the event_type.",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                help_text="This field is not the PK of the model. It is used to create EventSlot UUID for FRAB and iCal and other calendaring purposes.",
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="eventproposal",
            name="duration",
            field=models.IntegerField(
                blank=True,
                help_text="How much time (in minutes) should we set aside for this event?",
            ),
        ),
        migrations.AddConstraint(
            model_name="eventsession",
            constraint=django.contrib.postgres.constraints.ExclusionConstraint(
                expressions=[
                    ("event_location", "="),
                    ("event_type", "="),
                    ("when", "-|-"),
                ],
                name="prevent_adjacent_eventsessions",
            ),
        ),
    ]