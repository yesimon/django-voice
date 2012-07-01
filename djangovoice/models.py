from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _, pgettext

STATUS_CHOICES = (
    ('open', pgettext('status', 'Open')),
    ('closed', pgettext('status', 'Closed')),
)


class Status(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500)
    default = models.BooleanField(
        blank=True,
        help_text=_('New feedback will have this status'))
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="open")

    def save(self):
        if self.default == True:
            try:
                default_project = Status.objects.get(default=True)
                default_project.default = False
                default_project.save()
            except:
                pass
        super(Status, self).save()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("statuses")


class Type(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500)

    def __unicode__(self):
        return self.title


class Feedback(models.Model):
    type = models.ForeignKey(Type, verbose_name=_('Type'))
    title = models.CharField(max_length=500, verbose_name=_('Title'))
    description = models.TextField(
        blank=True,
        help_text=_('This wiill be viewable by other people - '\
                  'do not include any private details such as '\
                  'passwords or phone numbers here.')
        , verbose_name=_('Description')
        )
    anonymous = models.BooleanField(
        blank=True,
        help_text=_('Do not show who sent this')
        , verbose_name=_('Anonymous')
        )
    private = models.BooleanField(
        blank=True,
        help_text=_('Hide from public pages. Only site administrators '\
                  'will be able to view and respond to this.')
        , verbose_name=_('Private')
        )
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=_('User'))
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.ForeignKey(Status, verbose_name=_('Status'))
    duplicate = models.ForeignKey('self', null=True, blank=True, verbose_name=_('Duplicate'))

    def save(self, *args, **kwargs):
        try:
            self.status
        except:
            try:
                default = Status.objects.get(default=True)
            except:
                default = Status.objects.filter()[0]
            self.status = default
        super(Feedback, self).save()

    def get_absolute_url(self):
        return ('djangovoice_item', (self.id,))
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("feedback")
