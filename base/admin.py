from django.contrib import admin
from .models import User, Transactions, PayRequest
# Register your models here.

admin.site.register(User)
admin.site.register(Transactions)
admin.site.register(PayRequest)