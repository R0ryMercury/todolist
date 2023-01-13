from django.db import models


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

    class Meta:
        verbose_name = "tg пользователь"
        verbose_name_plural = "tg пользователи"
