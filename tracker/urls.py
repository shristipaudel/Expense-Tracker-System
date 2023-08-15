from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from budget.views import *
from expenses.views import *
from savings.views import *
from user.views import *
from rest_framework.authtoken import views

router = routers.DefaultRouter()

router.register(r'budget', BudgetViewset, 'budget')
router.register(r'expenses', ExpensesViewset, 'expenses')
router.register(r'savings', SavingViewset, 'saving')
# router.register(r'user', CustomuserViewset, 'saving')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/v1/', include(router.urls))
]
git remote add origin https://gitlab.com/mangosoftsolution/internship/expense-tracker/web.git
git add .
git commit -m "Initial commit"
git push -u origin master
