import uuid
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from djangovoice.models import Feedback, Type
from djangovoice.forms import WidgetForm, EditForm
from djangovoice.utils import paginate


def current_site_context(method):
    """Adds the current site and brand_view to the template context."""
    def wrapped(self, **kwargs):
        context = method(self, **kwargs)
        if Site._meta.installed:
            current_site = Site.objects.get_current()
        else:
            current_site = None
        context.setdefault('site', current_site)
        brand_view = getattr(settings, 'VOICE_BRAND_VIEW', 'djangovoice_home')
        context.setdefault('brand_view', brand_view)
        return context
    return wrapped


class FeedbackDetailView(DetailView):

    template_name = 'djangovoice/detail.html'
    model = Feedback

    @current_site_context
    def get_context_data(self, **kwargs):
        return super(FeedbackDetailView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        feedback = self.get_object()

        if feedback.private:
            # Anonymous private feedback can be only accessed with slug
            if not request.user.is_staff and 'slug' not in kwargs and feedback.user is None:
                return HttpResponseNotFound
            if not request.user.is_staff and request.user != feedback.user and feedback.user is not None:
                return HttpResponseNotFound

        return super(FeedbackDetailView, self).get(request, *args, **kwargs)


# FIXME: Can not we use ListView?
class FeedbackListView(TemplateView):

    template_name = 'djangovoice/list.html'

    @current_site_context
    def get_context_data(self, **kwargs):
        context = super(FeedbackListView, self).get_context_data(**kwargs)
        feedback = Feedback.objects.all().order_by('-created')
        feedback_list = kwargs.get('list', 'open')
        feedback_type = kwargs.get('type', 'all')
        feedback_status = kwargs.get('status', 'all')

        if feedback_list == 'open':
            title = _("Open Feedback")
            feedback = feedback.filter(status__status='open')
        elif feedback_list == 'closed':
            title = _("Closed Feedback")
            feedback = feedback.filter(status__status='closed')
        elif feedback_list == 'mine':
            title = _("My Feedback")
            feedback = feedback.filter(user=self.request.user)
        else:
            title = _("Feedback")

        if feedback_type != 'all':
            feedback = feedback.filter(type__slug=feedback_type)

        if feedback_status != 'all':
            feedback = feedback.filter(status__slug=feedback_status)

        # If user is checking his own feedback, do not filter by private
        if not self.request.user.is_staff and feedback_list != 'mine':
            feedback = feedback.filter(private=False)

        feedback_page = paginate(feedback, 10, self.request)

        context.update({
            'feedback_list': feedback_page.object_list,
            'pagination': feedback_page,
            'list': feedback_list,
            'status': feedback_status,
            'type': feedback_type,
            'navigation_active': feedback_list,
            'title': title
        })

        return context

    def get(self, request, *args, **kwargs):
        if kwargs.get('list') == 'mine' and not request.user.is_authenticated():
            return redirect(reverse('django.contrib.auth.views.login') + '?next=%s' % request.path)
        return super(FeedbackListView, self).get(request, *args, **kwargs)


class FeedbackWidgetView(FormView):

    template_name = 'djangovoice/widget.html'
    form_class = WidgetForm
    initial = {'type': Type.objects.get(pk=1)}

    def get(self, request, *args, **kwargs):
        return super(FeedbackWidgetView, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        return super(FeedbackWidgetView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        feedback = form.save(commit=False)
        if form.cleaned_data.get('anonymous') != 'on':
            feedback.user = self.request.user
        feedback.save()

        messages.add_message(
            self.request, messages.SUCCESS, _("Thanks for feedback."))

        return redirect('djangovoice_widget')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             _("Form is invalid."))

        return super(FeedbackWidgetView, self).form_invalid(form)


class FeedbackSubmitView(FormView):

    template_name = 'djangovoice/submit.html'
    form_class = WidgetForm

    @current_site_context
    def get_context_data(self, **kwargs):
        return super(FeedbackSubmitView, self).get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_anonymous() and not getattr(settings, 'VOICE_ALLOW_ANONYMOUS_USER_SUBMIT', False):
            return redirect(reverse('django.contrib.auth.views.login') + '?next=%s' % request.path)
        return super(FeedbackSubmitView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_anonymous() and not getattr(settings, 'VOICE_ALLOW_ANONYMOUS_USER_SUBMIT', False):
            return HttpResponseNotFound
        return super(FeedbackSubmitView, self).post(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(FeedbackSubmitView, self).get_form(form_class)
        if self.request.user.is_anonymous():
          del form.fields['anonymous']
          del form.fields['private']
        else:
          del form.fields['email']
        return form

    def form_valid(self, form):
        feedback = form.save(commit=False)
        if self.request.user.is_anonymous() and getattr(settings, 'VOICE_ALLOW_ANONYMOUS_USER_SUBMIT', False):
            feedback.private = True
        elif form.data.get('anonymous') != 'on':
            feedback.user = self.request.user

        if not feedback.user:
            feedback.slug = uuid.uuid1().hex[:10]

        feedback.save()

        # If there is no user, show the feedback with slug
        if not feedback.user:
            return redirect('djangovoice_slug_item', slug=feedback.slug)
        return redirect(feedback)


class FeedbackEditView(FormView):

    template_name = 'djangovoice/edit.html'

    def get_form_class(self):
        feedback = self.get_object()
        if self.request.user.is_staff:
            return EditForm
        elif self.request.user == feedback.user:
            return WidgetForm
        return None

    def get_object(self):
        return Feedback.objects.get(pk=self.kwargs.get('pk'))

    def get_form_kwargs(self):
        kwargs = super(FeedbackEditView, self).get_form_kwargs()
        kwargs.update({'instance': self.get_object()})

        return kwargs

    @current_site_context
    def get_context_data(self, **kwargs):
        return super(FeedbackEditView, self).get_context_data(**kwargs)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        if not form_class:
            raise HttpResponseNotFound

        return super(FeedbackEditView, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        return super(FeedbackEditView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        feedback = form.save()
        return redirect(feedback)


class FeedbackDeleteView(DeleteView):

    template_name = 'djangovoice/delete.html'

    def get_object(self):
        return Feedback.objects.get(pk=self.kwargs.get('pk'))

    @current_site_context
    def get_context_data(self, **kwargs):
        return super(FeedbackDeleteView, self).get_context_data(**kwargs)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # FIXME: should feedback user have delete permissions?
        feedback = self.get_object()
        if not request.user.is_staff and request.user != feedback.user:
            raise HttpResponseNotFound

        return super(FeedbackDeleteView, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        feedback = self.get_object()
        feedback.delete()

        return redirect('djangovoice_home')
