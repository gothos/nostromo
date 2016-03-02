from django.db import models
from django.contrib.postgres.fields import JSONField

class DataSet(models.Model):
    user = models.ForeignKey("account.User", related_name=u"datasets")

    types = (
        ("accel", "Accelerometer"),
        ("steps", "Steps"),
        ("run", "Running"),
        ("heart", "Heart rate"),
    )

    type = models.CharField(max_length=32, default="accel")

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    data = JSONField()

    class Meta:
        unique_together = (
            ("user", "start_date", "end_date"),
        )
        index_together = (
            ("user", "start_date", "end_date"),
            ("type", "start_date", "end_date"),
            ("start_date", "end_date"),
        )

