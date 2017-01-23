from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tracker.models import Mail,Log,Receiver
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import redirect
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
    # user = request.user
    # if user is not None:
        # return redirect('/')
    # return HttpResponse("Register")
    return render(request, 'registration/register.html')

# def register_view(request,message):
    # user = request.user
    # if user is not None:
        # return redirect('/')
    # return HttpResponse("Register")
    # return render(request, 'registration/register.html',{'message' : message})


# class RegistrationView(CreateView):
#     form_class = RegistrationForm
#     model = User

#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.set_password(User.objects.make_random_password())
#         obj.save()

#         # This form only requires the "email" field, so will validate.
#         reset_form = PasswordResetForm(self.request.POST)
#         reset_form.is_valid()  # Must trigger validation
#         # Copied from django/contrib/auth/views.py : password_reset
#         opts = {
#             'use_https': self.request.is_secure(),
#             'email_template_name': 'registration/verification.html',
#             'subject_template_name': 'registration/verification_subject.txt',
#             'request': self.request,
#             # 'html_email_template_name': provide an HTML content template if you desire.
#         }
#         # This form sends the email on save()
#         reset_form.save(**opts)
#         return redirect('accounts:register-done')

def register(request):
    if request.user.is_authenticated() and not request.user.is_anonymous():
        return redirect('/')

    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    if User.objects.filter(username = username).exists():
        # return render(request, 'registration/register.html',)
        # return register_view(request,message = "User already exists")
        return render(request, 'registration/register.html',{'message' : "User already exists"})
    if User.objects.filter(email = email).exists():
        # return register_view(request,message = "Email is already taken")
        return render(request, 'registration/register.html',{'message' : "Email is already taken"})
        # return redirect('/register/' , message = "Email is already taken")

    user = User.objects.create_user(username = username,password = password,first_name = firstname , last_name = lastname,email = email)

    if user is not None:
        auth_login(request, user)
    else:
        return render(request, 'registration/register.html',{'message' : "An error occured"})
        # return redirect('/register',message = "An error occured")

    # return HttpResponse(user)
    # handle exception
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
    # return HttpResponse('page : %s' % str(page))

    # if request.is_ajax():
    #     return HttpResponse(str(res))

    return render(request, 'index.html', {'mails': res,'start' : start , 'end' : end , 'total' : total , 'page' : page})

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