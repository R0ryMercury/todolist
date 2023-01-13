from django.core.management import BaseCommand
from todolist import settings


from bot.tg.client import TgClient
from bot.tg.dc import Message
from bot.models import TgUser


class Command(BaseCommand):
    help = "run bot"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_user_id=msg.from_.id,
            defaults={
                "tg_chat_id": msg.chat.id,
                "username": msg.from_.username,
            },
        )
        if created:
            self.tg_client.send_message(msg.chat.id, "[greeting]")
        else:
            self.tg_client.send_message(msg.chat.id, "[уже был]")
    def handle(self, *args, **kwargs):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)
