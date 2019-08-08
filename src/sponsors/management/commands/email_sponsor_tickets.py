# coding: utf-8
from django.core.management.base import BaseCommand
from django.utils import timezone

from camps.models import Camp
from sponsors.models import Sponsor
from sponsors.email import add_sponsorticket_email
from tickets.models import SponsorTicket, TicketType


class Command(BaseCommand):
    help = "Emails sponsor tickets"

    def add_arguments(self, parser):
        parser.add_argument("camp_slug", type=str)

    def output(self, message):
        self.stdout.write(
            "{}: {}".format(timezone.now().strftime("%Y-%m-%d %H:%M:%S"), message)
        )

    def handle(self, *args, **options):
        camp = Camp.objects.get(slug=options["camp_slug"])
        sponsors = Sponsor.objects.filter(tier__camp=camp, tickets_generated=True)

        for sponsor in sponsors:
            if (
                sponsor.tier.tickets and
                sponsor.tickets_generated and
                sponsor.ticket_email and
                sponsor.ticket_ready and
                not sponsor.tickets_sent
            ):
                self.output("# Generating outgoing email to send tickets for {}:".format(sponsor))
                # send the email
                if add_sponsorticket_email(sponsor=sponsor):
                    logger.info("OK: email to %s added" % sponsor)
                    sponsor.tickets_sent = True
                    sponsor.save()
                else:
                    logger.error("Unable to send sponsor ticket email to %s" % sponsor)

