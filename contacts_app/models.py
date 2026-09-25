from django.conf import settings
from django.db import models


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contacts',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name or ""}'.strip()
