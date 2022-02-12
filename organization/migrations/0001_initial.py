# Generated by Django 3.2.12 on 2022-02-05 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import helpers.db_helper


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=helpers.db_helper.generate_id,
                        editable=False,
                        max_length=70,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=60)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("religion", "religion"),
                            ("politics", "politics"),
                            ("music", "music"),
                            ("technology", "technology"),
                            ("sport", "sport"),
                            ("health", "health"),
                            ("entertainment", "entertainment"),
                            ("finance", "finance"),
                            ("others", "others"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="deleted by",
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        related_name="members",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="organization member",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="organization owner",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="updated by",
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "abstract": False,
            },
        ),
    ]