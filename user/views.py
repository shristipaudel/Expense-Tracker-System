from django.shortcuts import render, redirect
from .models import *
from .serializers import *
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.utils import timezone
from rest_framework import status as drf_status
import datetime

def Login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        # AuthenticationForm_can_also_be_used__
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            group = None
            perms=[]

            for item in user.get_user_permissions():
                app_label, codename = item.split('.')
                perms.append(Permission.objects.get(content_type__app_label=app_label, codename=codename))

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group or request.user.is_superuser:
                return redirect('api/')

            else:
				# i case i choose wrong role based on username and password
                messages.error(request, "Invalid User")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Details")
            return redirect('login')
    return render(request, 'authentication/login.html', {'form':form, 'title':'log in'})
