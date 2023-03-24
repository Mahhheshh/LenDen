# LenDen
LenDen is a Django app designed to help users manage their finances by keeping track of their lending and borrowing activities. With LenDen, users can easily record all of their transactions, including loans given or received, repayments, and outstanding balances.
 
# Features
* Record loans, repayments, and outstanding balances.
* View an overview of your cash flow.
* Monitor your loans.
* Search and filter transactions by date range, category, or other criteria.

# Installation
Python and Django need to be installed.
```
pip install -r requirements.txt
```

# Usage
Go to the LenDen folder and run
```
python manage.py runserver
```
Then go to the browser and enter the url [localhost:8000](http://localhost:8000/)

# Todo
- [ ] :bell: Add in-app notifications feature for new transactions
- [ ] :money_with_wings: Allow lenders to request money back from borrowers
- [ ] :bar_chart: Create a dashboard for visualizing transaction history
- [ ] :hammer_and_wrench: Improve the HTML structure of the web app.

# Preview
Signup
![signup](preview/signuppage.png)

Login
![login](preview/loginpage.png)

Dashboard
![dashboard](preview/dashboard.png)

Transactions
![Transactions](preview/transactionspage.png)

Add Loans
![add-loans](preview/addloanpage.png)

Make Payment Request
![make-pay_request](preview/makepayrequest.png)

Manage Payment Requests
![manage-request](preview/manage_pay_requests.png)


# License
LenDen is licensed under the [MIT License](https://github.com/Mahhheshh/LenDen/blob/main/LICENSE).