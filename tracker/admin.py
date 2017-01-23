from django.contrib import admin
from .models import Mail
from .models import Receiver
from .models import Log
from panel.models import Message

admin.site.register(Mail)
admin.site.register(Receiver)
admin.site.register(Log)
admin.site.register(Message)
