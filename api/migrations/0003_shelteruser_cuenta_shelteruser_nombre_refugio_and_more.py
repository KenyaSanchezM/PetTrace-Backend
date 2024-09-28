# Generated by Django 4.2.13 on 2024-09-27 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_shelteruser_descripcion"),
    ]

    operations = [
        migrations.AddField(
            model_name="shelteruser",
            name="cuenta",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="shelteruser",
            name="nombre_refugio",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="shelteruser",
            name="telefono_refugio",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
