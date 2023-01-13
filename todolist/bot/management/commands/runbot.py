from django.core.management import BaseCommand
from todolist import settings

from bot.tg.client import TgClient


class Command(BaseCommand):
    help = "run bot"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle(self, *args, **kwargs):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                print(item.message)
