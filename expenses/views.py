from ast import Return
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from .models import *
from budget.models import *
from .serializers import *
from decimal import Decimal
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db.models import Sum


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

class ExpensesViewset(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()  
    serializer_class = ExpensesSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    filterset_fields = ['id','name', 'budget','amount']
    search_fields = ['name', 'budget']
    ordering_fields = ['id']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if self.request.user.has_perm('expenses.view_expenses'):
            try:
                report = self.request.query_params['report']
            except:
                report = None
            if report:
                now = timezone.now()
                if report.lower() == 'daily':
                    return Expenses.objects.filter(created_at__date = now) 
                elif report.lower() == 'weekly':
                    #week_now = datetime.now().isocalendar()[1]
                    week_now = datetime.now().isocalendar().week
                    return Expenses.objects.filter(created_at__date__week = week_now)
                elif report.lower() == 'monthly':
                    return Expenses.objects.filter(created_at__date__month = now.strftime('%m'))
                elif report.lower() == 'yearly':
                    return Expenses.objects.filter(created_at__date__year = now.strftime('%Y')) 
                else:
                    return Expenses.objects.all()    
            else:
                return Expenses.objects.all()
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('expenses.view_expenses'):
            try:
                queryset = self.filter_queryset(self.get_queryset())
            except ObjectDoesNotExist :
                return Response('Expenses does not exist.', status = status.HTTP_400_BAD_REQUEST)
            if queryset:
                total = 0
                total = Expenses.objects.aggregate(Sum("amount"))
                return Response(total)
            else:
                return Response('Invalid request', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST) 
    
    def create(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('expenses.create_expenses'):
            amount = request.data['amount']
            try:
                budget = Budget.objects.get(id = request.data['budget'])
            except ObjectDoesNotExist :
                return Response('Invalid request.', status = status.HTTP_400_BAD_REQUEST)
            else:
                # import pdb;pdb.set_trace()
                budget.amount = budget.amount - Decimal(amount.replace(',','.'))
                # budget.save()
                if budget.amount == 0: 
                    return Response('Your budget is zero.', status = status.HTTP_400_BAD_REQUEST)
                elif budget.amount < Expenses.amount:
                    return Response('Your budget is insufficient', status=status.HTTP_400_BAD_REQUEST)
                elif (timezone.now() >= budget.end_date):
                    return Response('Your budget expired', status = status.HTTP_400_BAD_REQUEST)
                else:
                    return super().create(request, *args, **kwargs)   
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('expenses.view_expenses'):
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('expenses.change_expenses'):
            return super().update(request, *args, **kwargs)
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = get_user(request.auth)
        if user.has_perm('expenses.delete_expenses'):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response('Permission denied.', status = status.HTTP_400_BAD_REQUEST)

