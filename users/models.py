from io import BytesIO
import random

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone

from PIL import Image, ImageDraw, ImageFont

from core.constants import (
    AVATAR_BACKGROUND_COLORS,
    AVATAR_FILE_TEMPLATE,
    AVATAR_TEXT_COLOR,
    DEFAULT_AVATAR_FONT_SIZE,
    DEFAULT_AVATAR_SIZE,
    MAX_ABOUT_LENGTH,
    MAX_NAME_LENGTH,
    MAX_PHONE_LENGTH,
    MAX_SURNAME_LENGTH,
    PHONE_EXISTS_ERROR,
)
from core.validators import github_validator, phone_validator


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        name,
        surname,
        password=None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            name=name,
            surname=surname,
            **extra_fields,
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self,
        email,
        name,
        surname,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            email,
            name,
            surname,
            password,
            **extra_fields,
        )


def user_avatar_path(instance, filename):
    return f"avatars/user_{instance.id}/{filename}"


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
            self.avatar = self.generate_avatar()

            super().save(update_fields=["avatar"])

    def generate_avatar(self):
        image = Image.new(
            "RGB",
            DEFAULT_AVATAR_SIZE,
            random.choice(AVATAR_BACKGROUND_COLORS),
        )

        draw = ImageDraw.Draw(image)

        letter = self.name[0].upper()

        try:
            font = ImageFont.truetype(
                "arial.ttf",
                DEFAULT_AVATAR_FONT_SIZE,
            )
        except OSError:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), letter, font=font)

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        position = (
            (DEFAULT_AVATAR_SIZE[0] - text_width) // 2,
            (DEFAULT_AVATAR_SIZE[1] - text_height) // 2,
        )

        draw.text(
            position,
            letter,
            fill=AVATAR_TEXT_COLOR,
            font=font,
        )

        buffer = BytesIO()

        image.save(buffer, format="PNG")

        filename = AVATAR_FILE_TEMPLATE.format(
            email=self.email,
        )

        return ContentFile(
            buffer.getvalue(),
            name=filename,
        )

    def clean(self):
        phone = self.phone

        if phone is None:
            return

        if phone.startswith("8"):
            phone = "+7" + phone[1:]

        queryset = User.objects.filter(phone=phone)

        if self.pk:
            queryset = queryset.exclude(pk=self.pk)

        if queryset.exists():
            raise ValidationError({
                "phone": PHONE_EXISTS_ERROR,
            })

        self.phone = phone

    def __str__(self):
        return self.email
