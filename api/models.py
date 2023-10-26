from django.db import models

class Txn(models.Model):
    payer = models.CharField(max_length=520)
    receiver = models.CharField(max_length=520)
    action = models.JSONField()
    message = models.CharField(max_length=520)
    label = models.CharField(max_length=520)
    signature = models.CharField(max_length=520)

    def __str__(self) -> str:
        return self.receiver
