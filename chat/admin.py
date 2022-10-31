from django.contrib import admin
from .models import *

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id' ,  'name' ,'hosted_by' ,  'get_users' ,  'timestamp'  )
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('id' ,  'name' , 'isHosted' , 'status' , 'timestamp'  )

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id' , 'get_user' , 'get_room' ,  'content'  , 'timestamp' )

# Register your models here.
admin.site.register(Room ,RoomAdmin )
admin.site.register(User , UserAdmin)
admin.site.register(Message ,MessageAdmin )