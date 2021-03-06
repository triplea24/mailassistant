from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tracker.models import Mail,Log,Receiver
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from panel.models import Message
# Create your views here.

def index(request):
	# t = loader.get_template('index.html')
    # c = {'foo': 'bar'}
    # return HttpResponse(t.render(c, request), content_type='application/xhtml+xml')
    # return HttpResponse("Index")
    # user = request.user
    # if user is not None and user.is_authenticated:
    # user = request.user
    if request.user.is_authenticated():
        return redirect('/dashboard')
    return render(request, 'landing.html')

def register_view(request):
    return render(request, 'registration/register.html')

def register(request):
    if request.user.is_authenticated() and not request.user.is_anonymous():
        return redirect('/')

    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    if User.objects.filter(username = username).exists():
        return render_to_response(request, 'registration/register.html',{'message' : "User already exists"})
    if User.objects.filter(email = email).exists():
        return render(request, 'registration/register.html',{'message' : "Email is already taken"})

    user = User.objects.create_user(username = username,password = password,first_name = firstname , last_name = lastname,email = email)

    user = authenticate(username=username, password=password)

    if user is not None:
        auth_login(request, user)
    else:
        return render(request, 'registration/register.html',{'message' : "An error occured"})

    return redirect('/dashboard')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        # Redirect to a success page.
        return redirect('/dashboard')
    else:
        return redirect('/register/')
        # Return an 'invalid login' error message.

@login_required(login_url = '/register/')
def panel(request):
    # return HttpResponse("Panel")
    user = request.user


    mails = Mail.objects.filter(sender = user)

    total = Mail.objects.count()


    # res = []
    # datas = []
    # for mail in mails:
    #     to = Receiver.objects.filter(mail = mail , type_of_receiption = 'T')
    #     cc = Receiver.objects.filter(mail = mail , type_of_receiption = 'C')
    #     bcc = Receiver.objects.filter(mail = mail , type_of_receiption = 'B')
    #     # datas.append({})


    paginator = Paginator(mails, 5)

    page = request.GET.get('page')
    try:
        res = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        res = paginator.page(1)
        page = 1
    except EmptyPage:
        res = paginator.page(paginator.num_pages)
        page = paginator.num_pages
    start = res.start_index()
    end = res.end_index()

    tos = []
    ccs = []
    bccs = []
    for mail in res.object_list:
        to = Receiver.objects.filter(mail = mail , type_of_receiption = 'T')
        cc = Receiver.objects.filter(mail = mail , type_of_receiption = 'C')
        bcc = Receiver.objects.filter(mail = mail , type_of_receiption = 'B')
        tos.append(to)
        ccs.append(cc)
        bccs.append(bcc)

    # for mail in res:

    #     res.append({'mail':mail,'to':to,'cc':cc,'bcc':bcc})
    # return HttpResponse('page : %s' % str(page))
    # if request.is_ajax():
    #     return HttpResponse(str(res))

    return render(request, 'index.html', {'mails': res,'tos' : tos, 'ccs' : ccs, 'bccs' : bccs ,'start' : start , 'end' : end , 'total' : total , 'page' : page})

@login_required(login_url = '/register/')
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
def contact(request):
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']
    message = Message(name = name , email = email , message = message)
    message.save()
    return HttpResponse('')