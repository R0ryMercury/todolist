from todolist import settings
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class VerificationView(GenericAPIView):
    model = TgUser
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TgUserSerializer

    def patch(self, request, *args, **kwargs):
        ser: TgUserSerializer = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)

        tg_user: TgUser = ser.validated_data["tg_user"]
        tg_user.user = self.request.user
        tg_user.save(update_fields=["user"])
        instance_ser: TgUserSerializer = self.get_serializer(tg_user)
        tg_client = TgClient(settings.BOT_TOKEN)
        tg_client.send_message(tg_user.tg_chat_id, "[verification has been completed]")

        return Response(instance_ser.data)
