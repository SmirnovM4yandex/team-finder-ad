from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont
import random
import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            name=name,
            surname=surname,
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, name, surname, password, **extra_fields)


def user_avatar_path(instance, filename):
    return f"avatars/user_{instance.id}/{filename}"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)

    phone = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^(\+7|8)\d{10}$',
                message="Phone must be in format +7XXXXXXXXXX or 8XXXXXXXXXX"
            )
        ]
    )

    github_url = models.URLField(blank=True, null=True)
    about = models.TextField(max_length=256, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    favorites = models.ManyToManyField(
        "projects.Project",
        related_name="interested_users",
        blank=True
    )
    
    
    def save(self, *args, **kwargs):
        self.clean()

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and not self.avatar:
            self.avatar = self.generate_avatar()
            super().save(update_fields=["avatar"])


    def generate_avatar(self):
        size = (200, 200)

        colors = [
            (52, 152, 219),
            (46, 204, 113),
            (155, 89, 182),
            (241, 196, 15),
            (230, 126, 34),
            (231, 76, 60),
        ]

        bg_color = random.choice(colors)

        image = Image.new("RGB", size, bg_color)
        draw = ImageDraw.Draw(image)

        letter = self.name[0].upper()

        try:
            font = ImageFont.truetype("arial.ttf", 100)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        position = (
            (size[0] - text_width) // 2,
            (size[1] - text_height) // 2
        )

        draw.text(position, letter, fill="white", font=font)

        buffer = BytesIO()
        image.save(buffer, format="PNG")

        file_name = f"avatar_{self.email}.png"

        return ContentFile(buffer.getvalue(), name=file_name)
    

    def clean(self):
        # нормализация
        phone = self.phone
        if phone.startswith("8"):
            phone = "+7" + phone[1:]

        # проверка уникальности
        qs = User.objects.filter(phone=phone)
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError({"phone": "Phone already exists"})

        self.phone = phone
        

    def __str__(self):
        return self.email