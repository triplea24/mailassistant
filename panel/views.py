from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
	# t = loader.get_template('index.html')
    # c = {'foo': 'bar'}
    # return HttpResponse(t.render(c, request), content_type='application/xhtml+xml')
    return HttpResponse("This is the first page")
@login_required
def panel(request):
	return HttpResponse("Panel")