from channels.generic.websocket import  AsyncJsonWebsocketConsumer 
from asgiref.sync import sync_to_async

from .models import Room , Message , User

class ChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user_name = None 
        self.room_name = None 

        self.room = None
        self.user = None
        self.user_id = None
        
        self.isCreated = None 

    async def connect(self):
        print('connect')


        self.room_name = "_".join(self.scope['url_route']['kwargs']['room_name'].split())   #'url_route': {'args': (), 'kwargs': {'self.room_name': 'mk'}}}
        self.user_name = "_".join(self.scope['url_route']['kwargs']['user_name'].split() )
        self.isCreated = False  if self.scope['url_route']['kwargs']['choice'] == "join" else True 

        # print(self.room_name , self.user_name , self.isCreated)
        
        self.room , _  = Room.objects.get_or_create( name = self.room_name)
        self.user , _= User.objects.get_or_create( name = self.user_name  , isHosted = self.isCreated  )

        
        self.user_id = self.user.id 
        self.room.join(self.user)

        await self.channel_layer.group_add(self.room_name , self.channel_name)
        await self.accept()

        await self.send_json( {
                'type' : 'user_details_message' ,
                'user_id': self.user_id ,
                # 'room_id': self.room.id ,
                # 'room_name': self.room_name ,
                # 'user_name': self.user_name ,
            }  )


    async def disconnect(self, close_code):
        print('disconnect '  )

        self.room.leave(self.user)

        if(self.room.get_online_count() == 0 or self.isCreated ) :
            # Room.objects.filter( name = self.room_name ).delete()
            print('room is closed')

        await self.channel_layer.group_send(self.room_name,{ 
                'type':'leave.message' ,
                'command' : 'leave',
                'user_name': self.user_name ,
            })

        await self.close()


    async def receive_json(self, client_mess):

        command = client_mess['command']
        print('client_command : ' , command)
        
        if (command == 'join_room'):

            await self.channel_layer.group_send(self.room_name,{ 
                'type':'join.room.message' ,
                   'user_name': self.user_name ,
                'user_id': self.user_id ,
            })

        elif (command == 'offer'):

            await self.channel_layer.group_send(self.room_name,{
                'type':'offer.message' , 
                'offer':client_mess['offer'],
                'user_name': self.user_name ,

            })

        elif (command == 'answer'):

            await self.channel_layer.group_send(self.room_name,{
                'type':'answer.message' , 
                'answer':client_mess['answer'],
                'user_name': self.user_name ,

            })
            
        elif (command == 'candidate'):
            
            await self.channel_layer.group_send(self.room_name,{
                'type':'candidate.message' , 
                'candidate':client_mess['candidate'],
                'iscreated' : client_mess['iscreated'],
            })




    async def host_details_message(self , event):
        await self.send_json( event)

    async def joiner_details_message(self , event):
        await self.send_json( event)

    async def join_room_message(self , event):
        await self.send_json( event)
        
    async def leave_message(self , event):
        await self.send_json( event)

    async def offer_message(self , event):
                await self.send_json( event)

    async def answer_message(self , event):
                await self.send_json( event)

    async def candidate_message(self , event):
        await self.send_json( event)


'''
This is a asynchronous WebSocket consumer that accepts all connections, receives commands from its client, and echos those commands 
  back to the same client. For now it does not broadcast commands to other clients in the same self.room_name.
'''