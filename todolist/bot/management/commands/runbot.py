from django.core.management import BaseCommand
from todolist import settings


from bot.tg.client import TgClient
from bot.tg.dc import Message
from bot.models import TgUser
from goals.models import BoardParticipant, Goal, GoalCategory


class Command(BaseCommand):
    help = "run bot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle_user_without_verification(self, msg: Message, tg_user: TgUser):
        tg_user.set_verification_code()
        tg_user.save(update_fields=["verification_code"])
        self.tg_client.send_message(
            msg.chat.id, f"[verification code] {tg_user.verification_code}"
        )

    def fetch_goals(self, msg: Message, tg_user: TgUser):
        goals = Goal.objects.filter(user=tg_user.user)
        if goals.count() > 0:
            resp_msg = (f"#{goal.id} {goal.title}" for goal in goals)
            self.tg_client.send_message(msg.chat.id, "\n".join(resp_msg))
        else:
            self.tg_client.send_message(msg.chat.id, "[goals list is empty]")

    def fetch_cats(self, msg: Message, tg_user: TgUser):
        cats = GoalCategory.objects.filter(user=tg_user.user)
        if cats.count() > 0:
            info_msg = "Choose one of the categories bellow:"
            self.tg_client.send_message(msg.chat.id, info_msg)

            resp_msg = (f"#{cat.id} {cat.title}" for cat in cats)
            self.tg_client.send_message(msg.chat.id, "\n".join(resp_msg))

            tg_user.is_creating = True
            tg_user.save(update_fields=["is_creating"])
        else:
            self.tg_client.send_message(msg.chat.id, "[categories list is empty]")

    def choose_cat(self, msg: Message, tg_user: TgUser):
        cat = GoalCategory.objects.filter(user=tg_user.user, title=msg.text).first()
        if cat:
            resp_msg = f"you have selected a category {cat}"
            self.tg_client.send_message(msg.chat.id, resp_msg)

            tg_user.is_creating = False
            tg_user.cat_choosen = cat.title
            tg_user.save(update_fields=["is_creating", "cat_choosen"])

        else:
            resp_msg = f"The category '{msg.text}' does not exist"
            self.fetch_cats(msg, tg_user)

    def create_goal(self, msg: Message, tg_user: TgUser):
        board_participant = BoardParticipant.objects.filter(
            user=tg_user.user, role=BoardParticipant.Role.owner
        )

    def cancel(self, msg: Message, tg_user: TgUser):
        tg_user.is_creating = False
        tg_user.cat_choosen = None
        tg_user.save(update_fields=["is_creating", "cat_choosen"])
        self.tg_client.send_message(msg.chat.id, "[operation successfully canceled]")

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if not msg.text:
            return

        match msg.text.replace(" ", ""):
            case "/goals":
                self.fetch_goals(msg, tg_user)
            case "/create":
                self.fetch_cats(msg, tg_user)
            case "/cancel":
                self.cancel(msg, tg_user)
            case _:
                if tg_user.is_creating:
                    self.choose_cat(msg, tg_user)
                    return
                if tg_user.cat_choosen:
                    self.create_goal(msg, tg_user)
                    return

                self.tg_client.send_message(msg.chat.id, "[unknown command]")

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_id=msg.from_.id,
            defaults={
                "tg_chat_id": msg.chat.id,
                "username": msg.from_.username,
            },
        )
        if created:
            self.tg_client.send_message(msg.chat.id, "[greeting]")
        if tg_user.user:
            self.handle_verified_user(msg, tg_user)
        else:
            self.handle_user_without_verification(msg, tg_user)

    def handle(self, *args, **kwargs):
        offset = 0

        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)
