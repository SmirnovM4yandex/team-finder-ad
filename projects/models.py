from django.conf import settings
from django.db import models

from core.constants import (
    MAX_PROJECT_NAME_LENGTH,
    PROJECT_DESCRIPTION_MAX_LENGTH,
    PROJECT_STATUS_CHOICES,
    PROJECT_STATUS_OPEN,
    MAX_PROJECT_STATUS_LENGTH
)
from core.validators import github_validator


User = settings.AUTH_USER_MODEL


class Project(models.Model):
    name = models.CharField(
        max_length=MAX_PROJECT_NAME_LENGTH,
        verbose_name="Название",
    )

    description = models.TextField(
        max_length=PROJECT_DESCRIPTION_MAX_LENGTH,
        blank=True,
        verbose_name="Описание",
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Владелец",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    github_url = models.URLField(
        blank=True,
        null=True,
        validators=[github_validator],
        verbose_name="GitHub",
    )

    status = models.CharField(
        max_length=MAX_PROJECT_STATUS_LENGTH,
        choices=PROJECT_STATUS_CHOICES,
        default=PROJECT_STATUS_OPEN,
        verbose_name="Статус",
    )

    participants = models.ManyToManyField(
        User,
        related_name="participated_projects",
        blank=True,
        verbose_name="Участники",
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
