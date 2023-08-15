from ast import Delete
from calendar import month
from datetime import datetime, timedelta
from urllib import response
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status as drf_status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status
from decimal import Decimal
from rest_framework.authtoken.models import Token
from .models import Budget
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
#from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone
from django.db.models import Sum
#from rest_framework.filters import DjangoFilterBackend
#from django.utils import timespan
# Create your views here.

def get_user(token):
        try:
            user = Token.objects.get(key = token).user
        except ObjectDoesNotExist:
            return AnonymousUser
        else:
            return user

class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'l'
    offset_query_param = 'o'
    max_limit = 50

class BudgetViewset(viewsets.ModelViewSet):
    queryset = Budget.objects.all()  
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    authentication_classes = (TokenAuthentication,SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    filterset_fields = ['id','name','description','amount', 'created_at', 'updated_at','start_date','end_date']
    search_fields = ['name','description','start_date','end_date']
    ordering_fields = ['id']
    pagination_class = CustomPagination

    def get_queryset(self):
        if self.request.user.has_perm('budget.view_budget'):
            try:
                report = self.request.query_params['report']
            except:
                report = None
            if report:
                now = timezone.now()
                if report.lower() == 'daily':
                    return Budget.objects.filter(created_at__date = now) 
                elif report.lower() == 'weekly':
                    #week_now = datetime.now().isocalendar()[1]
                    week_now = datetime.now().isocalendar().week
                    return Budget.objects.filter(created_at__date__week = week_now)
                elif report.lower() == 'monthly':
                    return Budget.objects.filter(created_at__date__month = now.strftime('%m'))
                elif report.lower() == 'yearly':
                    return Budget.objects.filter(created_at__date__year = now.strftime('%Y')) 
                else:
                    return Budget.objects.all()    
            else:
              return Budget.objects.all()      
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

    # def list(self, request, *args, **kwargs):
    #     user = get_user(request.auth)
    #     if user.has_perm('budget.view_budget'):
    #         try:
    #             queryset = self.filter_queryset(self.get_queryset())
    #         except ObjectDoesNotExist :
    #             return Response('Expenses does not exist.', status = status.HTTP_400_BAD_REQUEST)
    #         else:
    #             total = 0
    #             total = Budget.objects.aggregate(Sum("amount"))
    #             return Response(total)
    #     else:
    #         return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('budget.create_budget'):
            amount = request.data['amount']
            if(Decimal(amount) == 0):
                return Response('Your budget is 0.', status = status.HTTP_400_BAD_REQUEST) 
            else:
                return super().create(request, *args, **kwargs)
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('budget.view_budget'):
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)
  
    def update(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('budget.change_budget'):
            return super().update(request, *args, **kwargs)
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('budget.delete_budget'):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

# class BudgetChoiceViewset(viewsets.ModelViewSet):
#     queryset = BudgetChoices.objects.all()  
#     serializer_class = BudgetChoiceSerializer
#     authentication_classes = (TokenAuthentication, SessionAuthentication)
#     permission_classes = (IsAuthenticated, )
#     filterset_fields = ['budget_choices', 'expiration_date']
#     search_fields = ['budget_choices', 'expiration_date']
#     ordering_fields = ['id']
#     pagination_class = LimitOffsetPagination

#     def list(self, request, *args, **kwargs):
#         user = get_user(request.auth)
#         if user.has_perm('budget.view_budgetchoice'):
#             return super().list(request, *args, **kwargs)
#         else:
#             return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

#     def create(self, request, *args, **kwargs):
#         user = get_user(request.auth)
#         if user.has_perm('budget.create_budgetchoice'):
#             return super().create(request, *args, **kwargs)
#         else:
#             return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)
   
#     def retrieve(self, request, *args, **kwargs):
#         user = get_user(request.auth)
#         if user.has_perm('budget.view_budgetchoice'):
#             return super().retrieve(request, *args, **kwargs)
#         else:
#             return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

#     def update(self, request, *args, **kwargs):
#         user = get_user(request.auth)
#         if user.has_perm('budget.change_budgetchoice'):
#             return super().update(request, *args, **kwargs)
#         else:
#             return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, *args, **kwargs):
#         user = get_user(request.auth)
#         if user.has_perm('budget.delete_budgetchoice'):
#             return super().destroy(request, *args, **kwargs)
#         else:
#             return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)


