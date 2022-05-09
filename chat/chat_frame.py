from channels import DEFAULT_CHANNEL_LAYER
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from channels.layers import get_channel_layer
import json


class Channel(AsyncWebsocketConsumer):
    room = "hacker-room"

    async def connect(self):
        await self.accept()
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close(code=1091)
        else:
            channels = ChatChannel.objects.filter(user=User.objects.get(id=user.id))
            if len(channels) > 0:
                await self.close(code=3000)
            else:
                await self.channel_layer.group_send(
                    self.room,
                    {
                        "type": "message",
                        "uid": user.id,
                        "code": 4000,
                    }
                )
                await self.channel_layer.group_add(self.room, self.channel_name)
                ChatChannel.objects.create(user=User.objects.get(id=user.id), channel=self.channel_name)

    async def forceremove(self, event):
        await self.close(3000)

    async def message(self, event):
        await self.send(json.dumps(event))

    async def receive(self, text_data=None, bytes_data=None):
        if not self.scope["user"].is_anonymous:
            messagedata = json.loads(text_data)
            layer = get_channel_layer(alias=DEFAULT_CHANNEL_LAYER)
            try:
                Chats.objects.create(sender=User.objects.get(id=self.scope["user"].id), receiver=User.objects.get(id=messagedata["userid"]), message=messagedata["data"])
                receiver = ChatChannel.objects.get(user=User.objects.get(id=messagedata["userid"]))
                await layer.send(receiver.channel, {
                    "type": "message",
                    "code": 2001,
                    "text": messagedata["data"],
                    "uid": self.scope["user"].id
                })
                await self.send(text_data=json.dumps({"code": 2000}))
            except ObjectDoesNotExist:
                await self.send(text_data=json.dumps({"code": 5000}))
        else:
            self.close(code=1091)

    async def disconnect(self, close_code):
        user = self.scope["user"]
        if not user.is_anonymous and close_code != 3000:
            ChatChannel.objects.filter(user=User.objects.get(id=user.id)).delete()
        await self.channel_layer.group_discard(self.room, self.channel_name)
        await self.channel_layer.group_send(self.room, {
            "type": "message",
            "code": 3006,
            "uid": self.scope["user"].id
        })
        await self.close(code=close_code)
