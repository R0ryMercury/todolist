from django.db import models
from secrets import choice
from string import ascii_letters, digits

CODE_CHOICES = ascii_letters + digits


class TgUser(models.Model):
    tg_id = models.BigIntegerField(verbose_name="tg id", unique=True)
    tg_chat_id = models.BigIntegerField(verbose_name="tg chat id")
    username = models.CharField(
        max_length=512, verbose_name="tg username", null=True, blank=True, default=None
    )
    user = models.ForeignKey(
        "core.User",
        models.PROTECT,
        null=True,
        blank=True,
        default=None,
        verbose_name="Пользователь в системе",
    )
    verification_code = models.CharField(
        max_length=32, verbose_name="код подтверждения", default=""
    )
    is_creating = models.BooleanField(default=False)
    cat_choosen = models.CharField(default=None, max_length=255, null=True, blank=True)

    def set_verification_code(self):
        code = "".join(choice(CODE_CHOICES) for _ in range(12))
        self.verification_code = code

    class Meta:
        verbose_name = "tg пользователь"
        verbose_name_plural = "tg пользователи"
