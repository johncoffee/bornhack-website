from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from utils.models import CampRelatedModel
from .email import add_new_membership_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
import logging
logger = logging.getLogger("bornhack.%s" % __name__)


class TeamArea(CampRelatedModel):
    class Meta:
        ordering = ['name']
        unique_together = ('name', 'camp')

    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    camp = models.ForeignKey('camps.Camp', related_name="teamareas", on_delete=models.PROTECT)
    responsible = models.ManyToManyField(
        'auth.User',
        related_name='responsible_team_areas'
    )

    def __str__(self):
        return '{} ({})'.format(self.name, self.camp)


class Team(CampRelatedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    area = models.ForeignKey(
        'teams.TeamArea',
        related_name='teams',
        on_delete=models.PROTECT
    )
    description = models.TextField()
    needs_members = models.BooleanField(default=True)
    members = models.ManyToManyField(
        'auth.User',
        related_name='teams',
        through='teams.TeamMember'
    )
    mailing_list = models.EmailField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return '{} ({})'.format(self.name, self.camp)

    def validate_unique(self, exclude):
        """
        We cannot use unique_together with the camp field because it is a property,
        so check uniqueness of team name and slug here instead
        """
        # check if this team name is in use under this camp
        if self.camp.teams.filter(name=self.name).exists():
            raise ValidationError("This Team name already exists for this Camp")
        if self.camp.teams.filter(slug=self.slug).exists():
            raise ValidationError("This Team slug already exists for this Camp")
        return True

    @property
    def camp(self):
        return self.area.camp

    def save(self, **kwargs):
        if (
            not self.pk or
            not self.slug
        ):
            slug = slugify(self.name)
            self.slug = slug

        super().save(**kwargs)

    def memberstatus(self, member):
        if member not in self.members.all():
            return "Not member"
        else:
            if TeamMember.objects.get(team=self, user=member).approved:
                return "Member"
            else:
                return "Membership Pending"

    @property
    def responsible(self):
        if TeamMember.objects.filter(team=self, responsible=True).exists():
            return User.objects.filter(
                teammember__team=self,
                teammember__responsible=True
            )
        else:
            return self.area.responsible.all()

    @property
    def anoncount(self):
        return self.approvedmembers.filter(user__profile__public_credit_name_approved=False).count()

    @property
    def approvedmembers(self):
        return TeamMember.objects.filter(team=self, approved=True)


class TeamMember(CampRelatedModel):
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    team = models.ForeignKey('teams.Team', on_delete=models.PROTECT)
    approved = models.BooleanField(default=False)
    responsible = models.BooleanField(default=False)

    def __str__(self):
        return '{} is {} member of team {}'.format(
            self.user, '' if self.approved else 'an unapproved', self.team
        )

    @property
    def camp(self):
        return self.team.camp


@receiver(post_save, sender=TeamMember)
def add_responsible_email(sender, instance, created, **kwargs):
    if created:
        if not add_new_membership_email(instance):
            logger.error('Error adding email to outgoing queue')


class TeamTask(CampRelatedModel):
    team = models.ForeignKey(
        'teams.Team',
        related_name='tasks',
        on_delete=models.PROTECT,
        help_text='The team this task belongs to',
    )
    name = models.CharField(
        max_length=100,
        help_text='Short name of this task',
    )
    slug = models.SlugField(
        max_length=255,
        blank=True,
        help_text='url slug, leave blank to autogenerate',
    )
    description = models.TextField(
        help_text='Description of the task. Markdown is supported.'
    )

    class Meta:
        ordering = ['name']
        unique_together = (('name', 'team'), ('slug', 'team'))

    def get_absolute_url(self):
        return reverse_lazy('teams:task_detail', kwargs={'camp_slug': self.team.camp.slug, 'team_slug': self.team.slug, 'slug': self.slug})

    @property
    def camp(self):
        return self.team.camp

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(**kwargs)

    @property
    def responsible(self):
        return self.team.responsible.all()

