from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone

from core.constants import (
    MAX_ABOUT_LENGTH,
    MAX_NAME_LENGTH,
    MAX_PHONE_LENGTH,
    MAX_SURNAME_LENGTH,
)
from core.validators import github_validator, phone_validator
from core.utils import (
    generate_avatar,
    user_avatar_path,
    validate_phone_uniqueness,
)
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
    )

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name="Имя",
    )

    surname = models.CharField(
        max_length=MAX_SURNAME_LENGTH,
        verbose_name="Фамилия",
    )

    avatar = models.ImageField(
        upload_to=user_avatar_path,
        blank=True,
        null=True,
        verbose_name="Аватар",
    )

    phone = models.CharField(
        max_length=MAX_PHONE_LENGTH,
        unique=True,
        validators=[phone_validator],
        blank=True,
        null=True,
        verbose_name="Телефон",
    )

    github_url = models.URLField(
        blank=True,
        null=True,
        validators=[github_validator],
        verbose_name="GitHub",
    )

    about = models.TextField(
        max_length=MAX_ABOUT_LENGTH,
        blank=True,
        verbose_name="О себе",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name="Сотрудник",
    )

    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата регистрации",
    )

    favorites = models.ManyToManyField(
        "projects.Project",
        related_name="interested_users",
        blank=True,
        verbose_name="Избранные проекты",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "name",
        "surname",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def save(self, *args, **kwargs):
        self.clean()

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.avatar:
            self.avatar = generate_avatar(self)

            super().save(
                update_fields=["avatar"],
            )

    def clean(self):
        validate_phone_uniqueness(self)

    def __str__(self):
        return self.email
