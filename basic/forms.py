from django.forms import ModelForm
from .models import Chatroom

class Chatroomform(ModelForm):
    class Meta:
        model = Chatroom
        fields ='__all__'
        exclude =['host','members']