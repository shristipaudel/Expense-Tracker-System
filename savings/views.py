from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.pagination import LimitOffsetPagination
from .models import Budget
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from .serializers import *
from decimal import Decimal
from datetime import datetime
from django.utils import timezone

def get_user(token):
        try:
            user = Token.objects.get(key = token).user
        except ObjectDoesNotExist:
            return AnonymousUser()
        else:
            return user

class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'l'
    offset_query_param = 'o'
    max_limit = 50
    
class SavingViewset(viewsets.ModelViewSet):
    queryset = Saving.objects.all()  
    serializer_class = SavingSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    filterset_fields = ['created_at','updated_at']
    search_fields = ['created_at']
    ordering_fields = ['id']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if self.request.user.has_perm('saving.view_saving'):
            try:
                report = self.request.query_params['report']
            except:
                report = None
            if report:
                now = timezone.now()
                if report.lower() == 'daily':
                    return Saving.objects.filter(created_at__date = now) 
                elif report.lower() == 'weekly':
                    #week_now = datetime.now().isocalendar()[1]
                    week_now = datetime.now().isocalendar().week
                    return Saving.objects.filter(created_at__date__week = week_now)
                elif report.lower() == 'monthly':
                    return Saving.objects.filter(created_at__date__month = now.strftime('%m'))
                elif report.lower() == 'yearly':
                    return Saving.objects.filter(created_at__date__year = now.strftime('%y')) 
                else:
                    return Saving.objects.all()    
            else:
                return Saving.objects.all()
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('expenses.view_expenses'):
            return super().list(request, *args, **kwargs)
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('savings.create_saving'):
            budget = request.data['budget']
            try:
                budget = Budget.objects.get(id = budget)
            except ObjectDoesNotExist :
                return Response('Budget does not exist.', status = status.HTTP_400_BAD_REQUEST)
            else:    
            # import pdb;pdb.set_trace()
                if budget.end_date < timezone.now():
                    if(budget.amount == 0): 
                        return Response('Your saving is zero.', status = status.HTTP_400_BAD_REQUEST)
                    else:
                        return super().create(request, *args, **kwargs) 
                else:
                    return Response('The budget is not expired yet!!', status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('savings.view_saving'):
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('savings.change_saving'):
            return super().update(request, *args, **kwargs)
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('savings.delete_saving'):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)