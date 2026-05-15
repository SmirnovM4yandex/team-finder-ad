MAX_NAME_LENGTH = 124
MAX_SURNAME_LENGTH = 124
MAX_PHONE_LENGTH = 12
MAX_ABOUT_LENGTH = 256

PROFILE_ABOUT_ROWS = 5

PHONE_REGEX = r"^(\+7|8)\d{10}$"

PHONE_ERROR_MESSAGE = (
    "Телефон должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX"
)

PHONE_EXISTS_ERROR = "Пользователь с таким номером уже существует"

DEFAULT_AVATAR_SIZE = (200, 200)
DEFAULT_AVATAR_FONT_SIZE = 100

AVATAR_BACKGROUND_COLORS = [
    (52, 152, 219),
    (46, 204, 113),
    (155, 89, 182),
    (241, 196, 15),
    (230, 126, 34),
    (231, 76, 60),
]

AVATAR_TEXT_COLOR = "white"

AVATAR_FILE_TEMPLATE = "avatar_{email}.png"

MAX_PROJECT_NAME_LENGTH = 200
PROJECT_DESCRIPTION_MAX_LENGTH = 5000
MAX_PROJECT_STATUS_LENGTH = 6

PROJECT_DESCRIPTION_ROWS = 6

PROJECT_STATUS_OPEN = "open"
PROJECT_STATUS_CLOSED = "closed"

PROJECT_STATUS_CHOICES = [
    (PROJECT_STATUS_OPEN, "Открыт"),
    (PROJECT_STATUS_CLOSED, "Закрыт"),
]

GITHUB_REGEX = (
    r"^https?:\/\/(www\.)?"
    r"github\.com\/[\w\-\.]+"
    r"(\/[\w\-\.]+)?\/?$"
)

GITHUB_ERROR_MESSAGE = (
    "Введите корректную ссылку на GitHub"
)

DEFAULT_PAGE_SIZE = 12

STATUS_OK = "ok"
STATUS_ERROR = "error"

PROJECT_CLOSED_MESSAGE = "Проект закрыт"

OWNER_CANNOT_LEAVE_MESSAGE = (
    "Владелец не может покинуть проект"
)

INVALID_CREDENTIALS_MESSAGE = (
    "Неверный email или пароль"
)

USER_FILTER_OWNERS_OF_FAVORITES = (
    "owners-of-favorite-projects"
)

USER_FILTER_OWNERS_OF_PARTICIPATING = (
    "owners-of-participating-projects"
)

USER_FILTER_INTERESTED_IN_MY_PROJECTS = (
    "interested-in-my-projects"
)

USER_FILTER_PARTICIPANTS_OF_MY_PROJECTS = (
    "participants-of-my-projects"
)