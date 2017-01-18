from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tracker.models import Mail,Log,Receiver
from django.shortcuts import redirect
# Create your views here.

@login_required(login_url = '/login/')
def index(request):
	# t = loader.get_template('index.html')
    # c = {'foo': 'bar'}
    # return HttpResponse(t.render(c, request), content_type='application/xhtml+xml')
    if(request.user.is_authenticated):
        return redirect('/dashboard')
    else:
        return redirect('/login')

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

    mails = Mail.objects.filter(sender = user)

    total = Mail.objects.count()


    paginator = Paginator(mails, 5)

    page = request.GET.get('page')
    try:
        res = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        res = paginator.page(1)
    except EmptyPage:
        res = paginator.page(paginator.num_pages)
    start = res.start_index()
    end = res.end_index()

    # return HttpResponse('page : %s' % str(page))

    return render(request, 'index.html', {'mails': res,'start' : start , 'end' : end , 'total' : total})

@login_required(login_url = '/login/')
def show(request,track_key):
    username = request.user.username

    mail = Mail.objects.filter(track_key = track_key)

    if len(mail) > 0:
        mail = mail[0]
    else:
        return redirect('/')

    tos = Receiver.objects.filter(mail = mail , type_of_receiption = 'T')
    ccs = Receiver.objects.filter(mail = mail , type_of_receiption = 'C')
    bccs = Receiver.objects.filter(mail = mail , type_of_receiption = 'B')

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
    return render(request, 'show.html', {'mail':mail,'tos' : tos, 'ccs' : ccs, 'bccs' : bccs , 'logs': logs , 'username' : username})