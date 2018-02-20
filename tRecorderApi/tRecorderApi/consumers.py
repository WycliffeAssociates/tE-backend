from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# from .exceptions import ClientError
# from .utils import get_room_or_error


class Consumer(WebsocketConsumer):
    """
    This chat consumer handles websocket connections for chat clients.

    It uses AsyncJsonWebsocketConsumer, which means all the handling functions
    must be async functions, and any sync work (like ORM access) has to be
    behind database_sync_to_async or sync_to_async. For more, read
    http://channels.readthedocs.io/en/latest/topics/consumers.html
    """

    ##### WebSocket event handlers

    def connect(self):
        async_to_sync(self.channel_layer.group_add)("translator", self.channel_name)
        # Accept the connection
        self.accept()




    def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """

    def upload_complete_message(self, event):
        self.send(text_data=event["text"])

    # ##### Handlers for messages sent over the channel layer
    #
    # # These helper methods are named by the types we send - so chat.join becomes chat_join
    # async def chat_join(self, event):
    #     """
    #     Called when someone has joined our chat.
    #     """
    #     # Send a message down to the client
    #     await self.send_json(
    #         {
    #             "msg_type": settings.MSG_TYPE_ENTER,
    #             "room": event["room_id"],
    #             "username": event["username"],
    #         },
    #     )
    #
    # async def chat_message(self, event):
    #     """
    #     Called when someone has messaged our chat.
    #     """
    #     # Send a message down to the client
    #     await self.send_json(
    #         {
    #             "msg_type": settings.MSG_TYPE_MESSAGE,
    #             "room": event["room_id"],
    #             "username": event["username"],
    #             "message": event["message"],
    #         },
    #     )
