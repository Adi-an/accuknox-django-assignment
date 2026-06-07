from django.db import models


class UserActivityLog(models.Model):
    """
    Represents a security-relevant user action in the system.
    Used to demonstrate Django signal behavior across Q1, Q2, Q3.
    """
    username = models.CharField(max_length=100)
    action = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} -> {self.action}"


class AlertRecord(models.Model):
    """
    An alert entry created inside a signal handler.
    Used in Q3 to verify whether signal DB writes share the caller's transaction.
    """
    triggered_by = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert: {self.message[:50]}"
