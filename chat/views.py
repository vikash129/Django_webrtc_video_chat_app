# chat/views.py
from django.shortcuts import render ,redirect
from .models import *
from django.views import View

def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



class IndexView(View):
    def post(self , request):
    
        room_name = request.POST['room']
        user_name = request.POST['name']
        choice = request.POST['choice']

        # print(request.POST)
        # print(room , name , choice)
        # <QueryDict: {'csrfmiddlewaretoken': ['xOmFDg2vIXdTFNQrTUbY2n5e21a5EmqKZUyO6z13X6NvvJfvWvf8LpjYRAqXZp5Q'], 'name': ['Vikash Kumar'], 'choice': ['created'], 'room': ['po']}>
        
        room , RoomCreated = Room.objects.get_or_create(  name = room_name   )

        print(room )

        if(choice == 'join'):
            if not RoomCreated :
                    return redirect( f"chat/{room_name}/join/{user_name}/{room.id}/")
            else:
                return render(request, "chat/index.html" ,{ "error_message" :'room not get' } )
        else:
            return redirect( f"chat/{room_name}/created/{user_name}/{room.id}")


            # return render(request, "chat/index.html" ,{ "error_message" :'room name already available' } )


    def  get(self , request ) :
        return render(request, "chat/index.html"  )
 




def room(request, room_name , created  , name  , id):

    context = {
                        "room_name": room_name ,
                        "isCreated" : created ,  
                        'name' : name ,
                        'chat_room_id' : id
                        }

    return render(request, "chat/room.html", context )

