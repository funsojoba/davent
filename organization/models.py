from django.db import models
from helpers.db_helper import BaseAbstractModel


class Organization(BaseAbstractModel):

    ORGANIZATION = (
        ("religion", "religion"),
        ("politics", "politics"),
        ("music", "music"),
        ("technology", "technology"),
        ("sport", "sport"),
        ("health", "health"),
        ("entertainment", "entertainment"),
        ("finance", "finance"),
        ("others", "others"),
    )

    name = models.CharField(max_length=60)
    owner = models.ForeignKey(
        "authentication.User",
        null=True,
        related_name="user",
        verbose_name="organization owner",
    )
    description = models.TextField(blank=True, null=True)
    category = models.CharField(choices=ORGANIZATION, max_length=255)
    members = models.ManyToManyField(
        "authentication.User",
        blank=True,
        null=True,
        related_name="members",
        verbose_name="organization member",
    )

    def __str__(self):
        return self.name
