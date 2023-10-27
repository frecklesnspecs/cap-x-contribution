from django.db import models

# Create your models here.
import datetime

from django.db import models
from django.utils import timezone


class Bug(models.Model):

    BUG_TYPE = [
        ("ERROR", "Error"),
        ("NEW FEATURE", "New Feature"),
        ("INTEGRATION", "Integration"),
        ("OTHER", "Other")
    ]

    STATUS = [
        ("TO DO", "To Do"),
        ("IN PROGRESS", "In Progress"),
        ("DONE", "Done"),
    ]

    description = models.TextField()
    bug_type = models.CharField(max_length=200, choices=BUG_TYPE)
    report_date = models.DateTimeField("Date Reported")
    status = models.CharField(max_length=200, choices=STATUS)

    def __str__(self):
        return self.description

    def was_reported_recently(self):
        return self.report_date >= timezone.now() - datetime.timedelta(days=1)
