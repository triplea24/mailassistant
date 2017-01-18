from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url = '/login/')
def index(request):
	# t = loader.get_template('index.html')
    # c = {'foo': 'bar'}
    # return HttpResponse(t.render(c, request), content_type='application/xhtml+xml')
    return HttpResponse("This is the first page")

def register(request):
	if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
	    variables = RequestContext(request, {
	    'form': form
	    })
    return render_to_response('registration/register.html',variables,)

@login_required(login_url = '/login/')
def panel(request):
	return HttpResponse("Panel")