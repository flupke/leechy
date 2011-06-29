from django.contrib import admin
from leechy.models import Leecher


class LeecherAdmin(admin.ModelAdmin):

    list_display = ("email", "name", "enabled", "invitation_sent",
            "date_created", "last_visit", "key")
    list_filter = ("enabled", "invitation_sent")


admin.site.register(Leecher, LeecherAdmin)
