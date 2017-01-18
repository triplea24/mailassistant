from django.contrib.auth.models import User, Group
from .models import Log,Mail
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
	# snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class MailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mail
        fields = ('subject', 'timestamp', 'sender' , 'track_key' , 'last_read','count')

class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = (
            'timestamp', 'device_ip',
            'device_browser','device_browser_family','device_browser_version','device_browser_version_string',
            'device_os','device_os_family','device_os_version','device_os_version_string',
            'device_type','device_type_family'
            )