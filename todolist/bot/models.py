from django.db import models


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField(verbose_name="tg chat id")
    tg_user_id = models.BigIntegerField(verbose_name="tg id", unique=True)
    user = models.ForeignKey(
        "core.User",
        models.PROTECT,
        null=True,
        blank=True,
        default=None,
        verbose_name="Пользователь в системе",
    )

    class Meta:
        verbose_name = "tg пользователь"
        verbose_name_plural = "tg пользователи"
