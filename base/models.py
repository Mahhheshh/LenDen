from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(null=True, default="avatar.svg", upload_to="media")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    def __str__(self) -> str:
        return f"{self.email}"


class Transactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    lender = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name="loan", null=True)
    borrower = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name="borrow", null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    description = models.CharField(max_length=150, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.id}: {self.lender} gave {self.borrower} for {self.description}"
    

class PayRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    amount = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    message = models.CharField(max_length=50, blank=True, null=True, default="Paid")
    transaction = models.ForeignKey(to=Transactions, null=True, on_delete=models.CASCADE, default=None)
    status = models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], default='Pending', max_length=10)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return self.status