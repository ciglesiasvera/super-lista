from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView

from super_lista.users.forms import UserRegistrationForm, UserProfileForm, ProfileForm
from super_lista.users.models import Profile


class RegisterView(CreateView):
    """User registration."""
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response


class ProfileView(LoginRequiredMixin, FormView):
    """View and edit user profile."""
    template_name = 'core/profile.html'
    success_url = reverse_lazy('profile')

    def get_form_class(self):
        return PasswordChangeForm if 'change_password' in self.request.POST else UserProfileForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = self.request.user
        if 'change_password' in self.request.POST:
            kwargs['user'] = user
        else:
            kwargs['instance'] = user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile, _ = Profile.objects.get_or_create(user=user)
        if 'profile_form' not in context:
            context['profile_form'] = ProfileForm(instance=profile)
        if 'password_form' not in context:
            context['password_form'] = PasswordChangeForm(user)
        return context

    def form_valid(self, form):
        if isinstance(form, PasswordChangeForm):
            form.save()
            update_session_auth_hash(self.request, form.user)
        else:
            form.save()
            # Also save profile
            profile = Profile.objects.get_or_create(user=self.request.user)[0]
            profile_form = ProfileForm(self.request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        context = self.get_context_data()
        if isinstance(form, PasswordChangeForm):
            context['password_form'] = form
        else:
            context['form'] = form
        return self.render_to_response(context)
