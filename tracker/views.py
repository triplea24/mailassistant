from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from .models import Log,Mail,Receiver
from .serializers import UserSerializer, GroupSerializer , MailSerializer, LogSerializer
from rest_framework import filters
from rest_framework import generics
import logging
from user_agents import parse as request_parser
from time import time
from datetime import datetime
from PIL import Image
from django.db import transaction


def new_mail(request):
    if request.user.is_authenticated():
        user = request.user
        timestamp = request.GET['timestamp']
        subject = request.GET['subject']
        count = 0
        track_key = request.GET['track_key']
            
        with transaction.atomic():
            mail = Mail(sender = user , timestamp = timestamp ,count = count , track_key = track_key)
            mail.save()
            tos = request.GET['tos']
            for to in tos:
                email = to['email']
                receiver = Receiver(mail = mail, email = email, type_of_receiption = 'T')
                receiver.save()
            ccs = request.GET['ccs']
            for cc in ccs:
                email = cc['email']
                receiver = Receiver(mail = mail, email = email, type_of_receiption = 'C')
                receiver.save()
            bccs = request.GET['ccs']
            for bcc in bccs:
                email = bcc['email']
                receiver = Receiver(mail = mail, email = email, type_of_receiption = 'B')
                receiver.save()

        return HttpResponse('')

def track(request,uuid):
    list_of_mails = Mail.objects.filter(track_key = uuid)
    print(get_client_ip(request))
    if len(list_of_mails) == 1:
        mail = list_of_mails[0]

        user_agent_str = request.META.get('HTTP_USER_AGENT')
        user_agent = request_parser(user_agent_str)
        device_ip = get_client_ip(request)

        device_browser = user_agent.browser
        device_browser_family = user_agent.browser.family
        device_browser_version_string = user_agent.browser.version_string
        device_os = user_agent.os
        device_os_family = user_agent.os.family
        device_os_version_string = user_agent.os.version_string
        device_type = user_agent.device
        device_type_family = user_agent.device.family

        log = Log(device_ip = device_ip, mail = mail,
            device_browser = device_browser, device_browser_family = device_browser_family,
            device_browser_version_string = device_browser_version_string,
            device_os = device_os,device_os_family=device_os_family,
            device_os_version_string = device_os_version_string,device_type = device_type,device_type_family = device_type_family)
        log.save()

        img = Image.new('RGB', (width, height))
        # img.putdata(my_list)
        # img.save('image.png')
        return HttpResponse(img, content_type="image/png")
    else:
        return HttpResponse("There is no such email")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class MailViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # queryset = Mail.objects.all().order_by('timestamp')
    serializer_class = MailSerializer
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Mail.objects.filter(sender=user)
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('sender')

class LogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = LogSerializer
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
    	# return Log.objects.all()
        user = self.request.user
        track_key = self.request.GET.get('track_key')
        mail = Mail.objects.filter(track_key = track_key)
        # mail = Mail.objects.all()[0]
        if mail is None:
        	print("mail is null! kiri!")
        else:
        	print(str("majid chaghal"))
        print(user.username)
        print(track_key)
        return Log.objects.filter(mail = mail)