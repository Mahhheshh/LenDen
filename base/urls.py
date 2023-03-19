from django.urls import path
from . import views

urlpatterns = [
    path("auth/signup/", views.signup, name="signup"),
    path("auth/login/", views.loginpage, name="loginpage"),
    path("logout/", views.logoutpage, name="logoutpage"),
    path("add/loan/", views.add_loan, name="add_loan"),
    path("view/profile/", views.profilepage, name="profilepage"),
    path("view/dashboard/", views.dashboard, name="dashboard"),
    path("view/transactions/", views.show_transactions, name="show_transactions"),
    path("view/request/", views.requestpage, name="requestpage"),
    path("pay/request/<transaction_id>", views.pay_request_view, name="pay_request_view"),
    path("ask/request/<transaction_id>", views.ask_request_view, name="ask_request_view"),
    path("manage/request/<request_id>", views.manage_request, name="manage_request"),
    path("cancel/request/<request_id>", views.cancel_request, name="cancel_request"),
]