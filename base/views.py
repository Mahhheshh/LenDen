from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm, UserSignupForm, UserLoginForm, UserUpdateFrom, PayRequestForm
from .models import Transactions, User, PayRequest
from django.db.models import Q, Sum
from django.contrib import messages
from .filters import TransactionFilter, RequestFilter

# Create your views here.
def signup(request):
    form = UserSignupForm()
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            login(request, user)
            user.save()
            return redirect('dashboard')
        else:
            messages.error(request, "Form is not Valid")
    return render(request, 'base/signup.html', {'form': form})

def loginpage(request):
    form = UserLoginForm()

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        email = request.POST.get("email").lower() 
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "Email does not exist's create new account insted")
            return redirect("signup")

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in as {request.user}")
            return redirect('dashboard')
        else:
            messages.error(request, "Username or Password does not match")
    return render(request, "base/loginform.html", context={"form":form})

@login_required(login_url="signup")
def logoutpage(request):
    logout(request) 
    return redirect('signup')

@login_required(login_url="signup")
def dashboard(request):
    transactions = Transactions.objects.filter(Q(lender=request.user.id)|Q(borrower=request.user.id))
    total_lenden_money = transactions.filter(Q(lender=request.user.id)&Q(is_paid=False)).aggregate(Sum('amount'))['amount__sum']
    total_borrowed_money = transactions.filter(Q(borrower=request.user.id)&Q(is_paid=False)).aggregate(Sum('amount'))['amount__sum']
    transactions = transactions[:7]
    context= {"lenden_money": total_lenden_money, "borrowed_money":total_borrowed_money, "transactions":transactions, "user":User}
    return render(request, "base/dashboard.html", context)

@login_required(login_url="signup")
def profilepage(request):
    form = UserUpdateFrom(instance=request.user)
    if request.method == "POST":
        form = UserUpdateFrom(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    context = {"form":form}
    return render(request, "base/settings.html", context)

@login_required(login_url="signup")
def show_transactions(request):
    transactions = request.user.loan.all() | request.user.borrow.all()
    users = User.objects.all()
    filter = TransactionFilter(request.GET, queryset=transactions, current_user=request.user)
    transactions = filter.qs
    context = {"transactions":transactions, "filter":filter, "users":users}
    return render(request, "base/transactionpage.html", context)

@login_required(login_url="signup")
def add_loan(request):
    form = TransactionForm(initial={"lender":request.user})
    context = {"form":form}
    if request.method == "POST":
        borrower = request.POST.get("borrower")
        if borrower == str(request.user.id):
            messages.error(request, "Can Not Lend Money To Yourself!")
            return redirect("add_loan")
        borrower = User.objects.get(id=borrower)
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        Transactions.objects.create(
            lender=request.user,
            borrower=borrower,
            amount=amount,
            description=description,
        )
        return redirect("show_transactions")
    return render(request, "base/loanform.html", context)

@login_required(login_url="signup")
def pay_request_view(request, transaction_id: str):
    try:
        transaction = Transactions.objects.get(id=transaction_id)
    except:
        messages.error(request, "Invalid Transaction")
        return redirect("dashboard")
    
    amount_paid = transaction.amount_paid
    amount_to_be_paid = transaction.amount - amount_paid
    form = PayRequestForm(initial={"amount":amount_to_be_paid, "amount_paid":amount_paid})
    context = {"form":form, "amount_paid": amount_paid}

    if request.method == "POST":
        form = PayRequestForm(request.POST)
        if form.is_valid():
            amount = float(form.cleaned_data.get("amount"))
            if amount <= 0:
                messages.error(request, "Amount should be greater than Zero")
                return redirect("pay_request_view", transaction_id=transaction_id)
            elif amount > (transaction.amount - amount_paid):
                messages.error(request, "Can not pay more than you borrowed")
                return redirect("pay_request_view", transaction_id=transaction_id)
            else:
                PayRequest.objects.create(
                    amount = form.cleaned_data.get("amount"),
                    message = form.cleaned_data.get("message", "-"),
                    transaction = transaction,
                )
                return redirect("requestpage")
    return render(request, "base/requestform.html", context)

@login_required(login_url="signup")
def ask_request_view(request, transaction_id):
    try:
        transaction = Transactions.objects.get(id=transaction_id)
    except:
        messages.error(request, "Invalid Transaction")
        return redirect("dashboard")
    
    amount_paid = transaction.amount_paid
    amount_to_be_paid = transaction.amount - amount_paid
    form = PayRequestForm(initial={"amount":amount_to_be_paid, "amount_paid":amount_paid})
    context = {"form":form, "amount_paid": amount_paid}

    if request.method == "POST":
        form = PayRequestForm(request.POST)
        if form.is_valid():
            amount = float(form.cleaned_data.get("amount"))
            if amount <= 0:
                messages.error(request, "Amount should be greater than Zero")
                return redirect("pay_request_view", transaction_id=transaction_id)
            elif amount > (transaction.amount - amount_paid):
                messages.error(request, "Can not Ask more than you lenden")
                return redirect("pay_request_view", transaction_id=transaction_id)
            else:
                PayRequest.objects.create(
                    amount = form.cleaned_data.get("amount"),
                    message = form.cleaned_data.get("message", "-"),
                    transaction = transaction,
                )
                return redirect("requestpage")
    return render(request, "base/askrequestform.html", context)

@login_required(login_url="signup")
def requestpage(request):
    requests = PayRequest.objects.filter(Q(transaction__lender=request.user)|Q(transaction__borrower=request.user))

    requests_filter = RequestFilter(request.GET, queryset=requests, current_user=request.user)
    requests = requests_filter.qs

    context = {"requests":requests, "filter":requests_filter}
    return render(request, "base/requestpage.html", context)

@login_required(login_url="signup")
def manage_request(request, request_id):
    pay_req = PayRequest.objects.get(id=request_id)
    if request.method == "POST":
        action = request.POST.get("action")
        if action in ["Approved", "Rejected"]:
            pay_req.transaction.amount_paid += pay_req.amount
            if pay_req.transaction.amount_paid == pay_req.transaction.amount:
                pay_req.transaction.is_paid = True
            pay_req.status = action
            pay_req.transaction.save()
            pay_req.save()
            return redirect("requestpage")
        else:
            messages.error(request, "Error While Processing The Data")
    context = {"pay_req":pay_req}
    return render(request, "base/manage_request.html", context)

@login_required(login_url="signup")
def cancel_request(request, request_id):
    try:
        req = PayRequest.objects.get(id=request_id)
    except:
        messages.error(request, "Request not found in database")
        return redirect('dashboard')
    req.delete()
    messages.success(request, "Pay Request Deleted Succefully")
    return redirect("requestpage")