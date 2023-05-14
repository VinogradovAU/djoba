from starlette.config import Config

config = Config(".env_dev")

DATABASES_URL = config("EE_DATABASE_URL", cast=str, default="")

SECRET_KEY = config("EE_SECRET_KEY", cast=str,
                    default="8f0742c8ad3faa0f7941e90e5bf3bfec426b1a10164cc58581824054267732e3")

ALGORITM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60
ADMIN_USERMANE = config("ADMIN_USERMANE", cast=str)
ADMIN_PASSWORD = config("ADMIN_PASSWORD", cast=str)
ADMIN_EMAIL = config("ADMIN_EMAIL", cast=str)


class Notification:
    def new_response(self):
        return "Получен новый отклик на объявление"

    def response_approved(self):
        return "Отклик одобрен"

    def joba_cancel(self):
        return "Поручение выполнено или отменено"

    def new_message(self):
        return "Получено новое сообщение"

    def new_stars(self):
        return "Вас оценили"

NOTIFICATIONS = Notification()