from django.db import models


class District(models.Model):
    """Data associated with a CalTrans District."""

    id = models.AutoField(primary_key=True)
    number = models.TextField(default="", blank=True, help_text="The number of the Caltrans district")
    name = models.TextField(default="", blank=True, help_text="The short name of the Caltrans district")

    def __str__(self):
        return f"{self.number} - {self.name}"
