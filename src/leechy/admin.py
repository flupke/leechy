from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.core.urlresolvers import reverse

from leechy.models import Leecher
from leechy import settings


def send_invitations(modeladmin, request, queryset):
    template = get_template("leechy/emails/invitation.txt")
    for leecher in queryset:
        context = Context({
            "innkeeper_name": settings.INNKEEPER_NAME,
            "leecher": leecher,
            "leecher_uri": request.build_absolute_uri(
                reverse("leechy_browse", 
                    kwargs={"key": leecher.key, "path": ""})),
        })
        send_mail(settings.INVITATION_SUBJECT, template.render(context),
                settings.INVITATION_EMAIL_FROM, [leecher.email])
        leecher.invitation_sent = True
        leecher.save()


send_invitations.short_description = _("Send invitations by email")


class LeecherAdmin(admin.ModelAdmin):

    list_display = ("email", "name", "enabled", "invitation_sent",
            "date_created", "last_visit", "share_link")
    list_filter = ("enabled", "invitation_sent")
    actions = [send_invitations]


admin.site.register(Leecher, LeecherAdmin)
