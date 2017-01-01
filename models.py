from django.db import models


class AdminEmail(models.Model):
    email_addr = models.CharField(max_length=80, default="", blank=True, null=True)

    def __str__(self):
        return self.email_addr
