from django.forms import ModelForm
from django import forms
from .models import Transactions, User, PayRequest
from django.contrib.auth.forms import UserCreationForm

class UserSignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm password','required': 'required'}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder': 'Confirm password','required': 'required'}

    class Meta:
        model = User
        fields = ("first_name", "last_name","email", "username", "password1","password2")
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "First Name"
                }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last Name"
                }),
            "email": forms.EmailInput(attrs={
                "class": "form-control", 
                "placeholder": "jhondoe@gmail.com"
                }),
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "User Name"
                }),
        }

class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ("email", "password")
        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control", 
                "placeholder": "jhondoe@gmail.com"
                }),
            "password": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Password"
                }),
        }

class UserUpdateFrom(ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "avatar")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control d-flex flex-column",
                "placeholder": "User Name"
                }),
            "email": forms.EmailInput(attrs={
                "class": "form-control", 
                "placeholder": "jhondoe@gmail.com"
                }),
        }

class TransactionForm(ModelForm):
    class Meta:
        model = Transactions
        fields =  ("lender", "borrower", "amount", "description")
        widgets = {
            "lender": forms.Select(attrs={
                "class":"form-select",
                "disabled":"disabled"
            }
            ),
            "borrower": forms.Select(attrs={
            "class":"form-select",
            "placeholder":"borrower-Name"
            }
            ),
            "amount": forms.NumberInput(attrs={
            "class":"form-contorl",
            "placeholder":"Amount",
            "required":"required",
            }
            ),
            "description": forms.Textarea(attrs={
            "class":"form-control",
            "placeholder":"Description",
            },
            )
        }

class PayRequestForm(ModelForm):
    class Meta:
        model = PayRequest
        fields = ("amount", "message")
        widgets = {
            "amount":forms.NumberInput(attrs={
            "class":"form-control",
            "Placeholder":"Amount",
            }
            ),
            "message":forms.Textarea(attrs={
            "class":"form-control",
            "Placeholder":"Message"
            })
        }