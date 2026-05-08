from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [('admin', 'Admin'), ('member', 'Member')]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        # Auto-set username to email if not set
        if not self.username:
            self.username = self.email
        # First user is admin
        if not self.pk and not User.objects.exists():
            self.role = 'admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['first_name', 'last_name']