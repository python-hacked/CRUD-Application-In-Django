import json
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView, View
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect
import pymysql
from django.contrib import messages

# API
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated   
from rest_framework import status
from django.contrib.auth.models import User
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer,ChangePasswordSerializer

# LOGIN APIwelcome
from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

# signal hera

from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from id.models import Person


# THIS IS USE FOR SIGNAL ONLY
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
# END OF THE SIGNAL


# Create your views here.

def view(request):
    render('home.html')


def login_page(request):
    return render(request, 'id/login.html')


def welcome_page(request):
    return render(request, 'id/welcome.html')


def index(request):
    return render(request, 'id/home.html', context={})


def home(request):
    return render(request, 'id/login.html', context={})


def successful(request):
    return render(request, 'id/welcome.html', context={})

# THIS IS ONLY FOR STARTING Response FOR ALL PAGES
def home(request):
    return ("this is my first page.")


def login(request):
    return ("this is my first page.")


def welcome(request):
    return ("this is my first page.")


def dataon(request):
    return ("this is my first page.")

# THIS IS ALL DATA VIEW
class AboutUs(View):
    def get(self, request, *args, **kwargs):
        return render(request, "home.html")


class loginus(View):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html")


class welcomeus(View):
    def get(self, request, *args, **kwargs):
        return render(request, "welcome.html")


class dataus(View):
    def get(self, request, *args, **kwargs):
        return render(request, "table.html")


#  create Ragistration form
def form_data(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        Company_name = request.POST['company']
        Email_name = request.POST['Email']
        Phone_number = request.POST['Phone']
        Password = make_password(request.POST['Password'])
        if Person.objects.filter(Phone_number=Phone_number).exists():
            messages.error(request, "phone number already exists")
            return redirect('/')

        elif Person.objects.filter(Email_name=Email_name).exists():
            messages.error(request, "Email id already exists")
            return redirect('/')

        else:
            Person.objects.create(first_name=first_name,
                                  last_name=last_name, Company_name=Company_name,
                                  Email_name=Email_name, Phone_number=Phone_number, Password=Password)
            return redirect('/login/')


# create login form
def Login_form(request):
    if request.method == 'POST':
        Phone_number = request.POST['Phone']
        User_Password = request.POST['Password']
        if Person.objects.filter(Phone_number=Phone_number).exists():
            obj = Person.objects.get(Phone_number=Phone_number)
            Password = obj.Password
            if check_password(User_Password, Password):
                return redirect('/welcome/')
            else:
                return HttpResponse('password incorrect')
        else:
            return HttpResponse('phone number is not registered')


# THIS IS CLIENT Authentication SYSTEM
# create Table data form
def data(request):
    persons = Person.objects.filter(is_active=True).order_by('id')

    return render(request, 'id/table.html', context={
        'request': request,
        'persons': persons,
    })


# create delete button
def delete_user(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        uid = json.loads(data)
        if Person.objects.filter(id=uid).exists():
            Person.objects.filter(id=uid).update(is_active=False)
            return JsonResponse({"staus": True, "message": "User has been deleted"})
        else:
            return JsonResponse({"staus": False, "message": "User not exists."})
    else:
        return JsonResponse({"staus": False, "message": "Method not allowed."})


# create Edit button
def update_view(request, uid):
    res = Person.objects.get(id=uid)
    return render(request, 'id/update.html', context={

        'person': res,
    })


# USE UPDATE DATA
def update_form_data(request):
    if request.method == 'POST':
        uid = request.POST['uid']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        Company_name = request.POST['company']
        Email_name = request.POST['Email']
        Phone_number = request.POST['Phone']

        Person.objects.filter(id=uid).update(first_name=first_name,
                                             last_name=last_name, Company_name=Company_name,
                                             Email_name=Email_name, Phone_number=Phone_number)
        return redirect('/data/')
        # redirect to table form    AND OF THE CLIENT TABLE


# THIS IS API SYSTEM
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "users": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })
        

# LOGIN API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        users = serializer.validated_data['users']
        # login(users)
        return super(LoginAPI, self).post(request, format=None)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
