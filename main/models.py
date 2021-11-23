from django.conf import settings
from django.db import models
from datetime import datetime


class Leave(models.Model):
    APPROVED_STATUS = (
        ('Y', 'Approve'),
        ('P', 'Pending'),
    )
    leave_text = models.CharField(max_length=200, verbose_name="reason for leave")
    leave_approved_status = models.CharField(max_length=1, choices=APPROVED_STATUS, default='P')
    leave_taken_date = models.DateField()
    leave_month = models.CharField(max_length=10, null=True, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.leave_taken_date:
            self.leave_month = self.leave_taken_date.strftime("%B")
        super(Leave, self).save(*args, **kwargs)

    class Meta:
        db_table = 'leave'
