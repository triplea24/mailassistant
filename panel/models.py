from django.db import models

# Create your models here.
class Message(models.Model):
	# keyLength = 36
	# sender = models.ForeignKey(User)
	timestamp = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length = 255)
	message = models.TextField()
	email = models.EmailField()
	# last_read = models.DateTimeField(blank = True , null = True)
	# count = models.IntegerField(default = 0)
	# track_key = models.CharField(max_length = keyLength, unique = True , blank = True)