from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Mail(models.Model):
	keyLength = 36
	sender = models.ForeignKey(User)
	timestamp = models.DateTimeField(null=True)
	subject = models.TextField()
	last_read = models.DateTimeField(blank = True)
	count = models.IntegerField(default = 0)
	track_key = models.CharField(max_length = keyLength, unique = True , blank = True)
	
class Receiver(models.Model):
	mail = models.ForeignKey(Mail)
	email = models.EmailField()
	typesOfReceiption = (
		('T','TO'),
		('C','CC'),
		('B','BCC'),
	)
	type_of_receiption = models.CharField(max_length = 1 , choices = typesOfReceiption , default = 'T')

class Log(models.Model):
	timestamp = models.DateTimeField(auto_now_add = True)
	mail = models.ForeignKey(Mail)
	url = models.TextField(blank = True)
	device_ip = models.IPAddressField(blank=True)
	device_browser = models.TextField(blank = True)
	device_browser_family = models.TextField(blank = True)
	device_browser_version_string = models.TextField(blank = True)
	device_os = models.TextField(blank = True)
	device_os_family = models.TextField(blank = True)
	device_os_version_string = models.TextField(blank = True)
	device_type = models.TextField(blank = True)
	device_type_family = models.TextField(blank = True)
@receiver(post_save, sender=Log, dispatch_uid="update_track_counter")
def update_track(sender, instance, **kwargs):
	instance.mail.count += 1
	instance.mail.last_read = instance.timestamp
	instance.mail.save()