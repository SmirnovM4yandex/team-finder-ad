from io import BytesIO
import random

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile

from PIL import Image, ImageDraw, ImageFont

from core.constants import (
    AVATAR_BACKGROUND_COLORS,
    AVATAR_FILE_TEMPLATE,
    AVATAR_TEXT_COLOR,
    DEFAULT_AVATAR_FONT_SIZE,
    DEFAULT_AVATAR_SIZE,
    PHONE_EXISTS_ERROR,
)


def user_avatar_path(instance, filename):
    return (
        f"avatars/user_{instance.id}/{filename}"
    )


def generate_avatar(user):
    image = Image.new(
        "RGB",
        DEFAULT_AVATAR_SIZE,
        random.choice(
            AVATAR_BACKGROUND_COLORS
        ),
    )

    draw = ImageDraw.Draw(image)

    letter = user.name[0].upper()

    try:
        font = ImageFont.truetype(
            "arial.ttf",
            DEFAULT_AVATAR_FONT_SIZE,
        )
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox(
        (0, 0),
        letter,
        font=font,
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = (
        (
            DEFAULT_AVATAR_SIZE[0]
            - text_width
        ) // 2,
        (
            DEFAULT_AVATAR_SIZE[1]
            - text_height
        ) // 2,
    )

    draw.text(
        position,
        letter,
        fill=AVATAR_TEXT_COLOR,
        font=font,
    )

    buffer = BytesIO()

    image.save(
        buffer,
        format="PNG",
    )

    filename = AVATAR_FILE_TEMPLATE.format(
        email=user.email,
    )

    return ContentFile(
        buffer.getvalue(),
        name=filename,
    )


def normalize_phone(phone):
    if phone.startswith("8"):
        return "+7" + phone[1:]

    return phone


def validate_phone_uniqueness(user):
    phone = user.phone

    if not phone:
        user.phone = None
        return

    phone = normalize_phone(phone)

    queryset = user.__class__.objects.filter(
        phone=phone,
    )

    if user.pk:
        queryset = queryset.exclude(
            pk=user.pk,
        )

    if queryset.exists():
        raise ValidationError({
            "phone": PHONE_EXISTS_ERROR,
        })

    user.phone = phone
