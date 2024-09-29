# Generated by Django 4.2.13 on 2024-09-29 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_eventadvertisement"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventadvertisement",
            name="imagen_evento",
            field=models.ImageField(
                blank=True,
                default="temp_image.jpg",
                null=True,
                upload_to="event_images/",
            ),
        ),
        migrations.AlterField(
            model_name="eventadvertisement",
            name="anfitrion_evento",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="eventadvertisement",
            name="motivo",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]