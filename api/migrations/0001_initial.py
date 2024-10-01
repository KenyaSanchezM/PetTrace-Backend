# Generated by Django 5.0.6 on 2024-10-01 19:22

import api.models.shelter_user
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="email address"
                    ),
                ),
                ("nombre", models.CharField(max_length=255)),
                ("telefono", models.CharField(max_length=15)),
                ("user_type", models.CharField(default="user", max_length=20)),
                (
                    "profile_image",
                    models.ImageField(blank=True, null=True, upload_to="users_images/"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ShelterUser",
            fields=[
                (
                    "user_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("estado", models.CharField(blank=True, max_length=128, null=True)),
                ("ciudad", models.CharField(blank=True, max_length=128, null=True)),
                ("direccion", models.CharField(blank=True, max_length=128, null=True)),
                (
                    "codigoPostal",
                    models.CharField(
                        blank=True,
                        max_length=5,
                        null=True,
                        validators=[api.models.shelter_user.validate_postal_code],
                    ),
                ),
                (
                    "descripcion",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                ("cuenta", models.CharField(blank=True, max_length=25, null=True)),
                (
                    "image1",
                    models.ImageField(blank=True, null=True, upload_to="users_images/"),
                ),
                (
                    "image2",
                    models.ImageField(blank=True, null=True, upload_to="users_images/"),
                ),
                (
                    "image3",
                    models.ImageField(blank=True, null=True, upload_to="users_images/"),
                ),
            ],
            options={
                "verbose_name": "Shelter User",
                "verbose_name_plural": "Shelter Users",
            },
            bases=("api.user",),
        ),
        migrations.CreateModel(
            name="DogPrediction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("breeds", models.CharField(max_length=255)),
                (
                    "image",
                    models.ImageField(
                        default="temp_image.jpg", upload_to="dog_images/"
                    ),
                ),
                (
                    "profile_image1",
                    models.ImageField(blank=True, null=True, upload_to="dog_images/"),
                ),
                (
                    "profile_image2",
                    models.ImageField(blank=True, null=True, upload_to="dog_images/"),
                ),
                ("estado", models.CharField(blank=True, max_length=128, null=True)),
                ("ciudad", models.CharField(blank=True, max_length=128, null=True)),
                ("direccion", models.CharField(blank=True, max_length=128, null=True)),
                ("tieneCollar", models.CharField(blank=True, max_length=255)),
                ("nombre", models.CharField(blank=True, max_length=255)),
                ("edad", models.CharField(blank=True, max_length=50)),
                ("color", models.CharField(blank=True, max_length=255)),
                ("caracteristicas", models.TextField(blank=True)),
                ("fecha", models.DateField(blank=True)),
                ("form_type", models.CharField(blank=True, max_length=255)),
                (
                    "sexo",
                    models.CharField(
                        choices=[("Macho", "Macho"), ("Hembra", "Hembra")], max_length=6
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EventAdvertisement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre_evento", models.CharField(max_length=255)),
                ("descripcion_evento", models.CharField(max_length=255)),
                ("lugar_evento", models.CharField(max_length=255)),
                ("motivo", models.CharField(blank=True, max_length=255)),
                ("anfitrion_evento", models.CharField(blank=True, max_length=255)),
                ("fecha_evento", models.DateField()),
                ("hora_evento", models.TimeField()),
                (
                    "imagen_evento",
                    models.ImageField(blank=True, null=True, upload_to="event_images/"),
                ),
                (
                    "refUser",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="api.shelteruser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DogPredictionShelter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("breeds", models.CharField(max_length=255)),
                (
                    "image",
                    models.ImageField(
                        default="temp_image.jpg", upload_to="dog_images/"
                    ),
                ),
                (
                    "profile_image1",
                    models.ImageField(blank=True, null=True, upload_to="dog_images/"),
                ),
                (
                    "profile_image2",
                    models.ImageField(blank=True, null=True, upload_to="dog_images/"),
                ),
                ("nombre", models.CharField(blank=True, max_length=255)),
                ("edad", models.CharField(blank=True, max_length=50)),
                ("color", models.CharField(blank=True, max_length=255)),
                ("caracteristicas", models.TextField(blank=True)),
                ("sexo", models.CharField(blank=True, max_length=50)),
                ("tamanio", models.CharField(blank=True, max_length=50)),
                ("temperamento", models.CharField(blank=True, max_length=100)),
                ("vacunas", models.CharField(blank=True, max_length=255)),
                ("esterilizado", models.CharField(blank=True, max_length=10)),
                (
                    "shelter_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.shelteruser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserDogRelationship",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_mine", models.BooleanField(default=False)),
                (
                    "dog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.dogprediction",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "dog")},
            },
        ),
    ]
