from django.db import models

status = (("Active","Active"),("Inactive","Inactive"),("Delete","Delete"))

class User(models.Model):
    name = models.CharField(max_length=20)
    isHosted = models.BooleanField(default=False)
    status = models.CharField(max_length=10,choices=status,default='Active')
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)


    def __str__(self):
        return self.name 


class Room(models.Model):
    name = models.CharField(max_length=12)
    online_users = models.ManyToManyField(to=User, blank=True)
    allowed_users = models.IntegerField(default=2)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.CharField(max_length=10,choices=status,default='Active')


    def get_online_count(self):
        return self.online_users.count()

    def join(self, user):
        self.online_users.add(user)
        self.save()

    def leave(self, user):
        self.online_users.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name}'

    def get_users(self):
        return ','.join(  [user.name for user in self.online_users.all()] )

    def hosted_by(self):
        return ''.join([user.name  for user in self.online_users.all() if user.isHosted ])



class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name}({self.room.name}): {self.content} '

    def get_user(self ):
        return f'{self.user.name}'

    def get_room(self ):
        return f'{self.room.name}'
