from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

@login_required(login_url = '/login/')
def index(request):
	# t = loader.get_template('index.html')
    # c = {'foo': 'bar'}
    # return HttpResponse(t.render(c, request), content_type='application/xhtml+xml')
    return HttpResponse("This is the first page")

def register(request):
    return HttpResponse("Register")
# 	if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = User.objects.create_user(
#             username=form.cleaned_data['username'],
#             password=form.cleaned_data['password1'],
#             email=form.cleaned_data['email']
#             )
#             return HttpResponseRedirect('/register/success/')
#     else:
#         form = RegistrationForm()
# 	    variables = RequestContext(request, {
# 	    'form': form
# 	    })
#     return render_to_response('registration/register.html',variables,)

@login_required(login_url = '/login/')
def panel(request):
    # return HttpResponse("Panel")
    user = request.user
    mails = Log.objects.filter(mail = mail)
    paginator = Paginator(mail, 5)

    page = request.GET.get('page')
    try:
        res = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        res = paginator.page(1)
    except EmptyPage:
        res = paginator.page(paginator.num_pages)
	return render(request, 'index.html', {'mails': res})

@login_required(login_url = '/login/')
def show(request,track_id):
    mail = Mail.objects.filter(track_id = track_id)
    logs = Log.objects.filter(mail = mail)
    paginator = Paginator(logs, 5)

    page = request.GET.get('page')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        logs = paginator.page(1)
    except EmptyPage:
        logs = paginator.page(paginator.num_pages)
    return render(request, 'show.html', {'logs': logs})