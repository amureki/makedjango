from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModelMixin(models.Model):
    modified_date = models.DateTimeField(
        _("modified date"),
        auto_now=True,
        editable=False,
        db_index=True,
    )
    created_date = models.DateTimeField(
        _("created date"),
        auto_now_add=True,
        editable=False,
        db_index=True,
    )

    class Meta:
        ordering = ("-modified_date", "-created_date")
        get_latest_by = "created_date"
        abstract = True
