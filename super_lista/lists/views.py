import uuid
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, View,
)
from django.http import Http404, JsonResponse

from super_lista.core.models import AuditEvent
from super_lista.lists.forms import ShoppingListForm, ShareListForm
from super_lista.lists.models import ShoppingList, ListMember, Invitation
from super_lista.lists.permissions import (
    ListAccessMixin,
    EditorRequiredMixin,
    OwnerRequiredMixin,
    get_user_role,
    can_view,
)


class ShoppingListListView(LoginRequiredMixin, ListView):
    """List all lists the user has access to, with pagination."""
    model = ShoppingList
    template_name = 'lists/list_list.html'
    context_object_name = 'lists'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        owned = ShoppingList.objects.filter(owner=user)
        shared = ShoppingList.objects.filter(members__user=user)
        return (owned | shared).distinct().order_by('-created_at')


class ShoppingListDetailView(ListAccessMixin, DetailView):
    """Show list with items and members."""
    model = ShoppingList
    template_name = 'lists/list_detail.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopping_list = self.object
        context['items'] = shopping_list.items.all()
        context['members'] = shopping_list.members.select_related('user').all()
        context['purchases'] = shopping_list.purchases.all()[:5]
        context['user_role'] = self.list_role
        return context


class ShoppingListCreateView(LoginRequiredMixin, CreateView):
    """Create a new shopping list."""
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = 'lists/list_form.html'
    success_url = reverse_lazy('list_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        # Auto-create owner membership
        ListMember.objects.create(
            list=self.object,
            user=self.request.user,
            role=ListMember.RoleChoices.OWNER,
            invited_by=self.request.user,
            accepted_at=timezone.now(),
        )
        AuditEvent.log(
            actor=self.request.user,
            entity_type='ShoppingList',
            entity_id=self.object.id,
            action='create',
        )
        messages.success(self.request, 'Lista creada exitosamente.')
        return response


class ShoppingListUpdateView(EditorRequiredMixin, UpdateView):
    """Edit a shopping list."""
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = 'lists/list_form.html'

    def get_success_url(self):
        return reverse('list_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        AuditEvent.log(
            actor=self.request.user,
            entity_type='ShoppingList',
            entity_id=self.object.id,
            action='update',
        )
        messages.success(self.request, 'Lista actualizada exitosamente.')
        return response


class ShoppingListDeleteView(OwnerRequiredMixin, DeleteView):
    """Delete a shopping list."""
    model = ShoppingList
    template_name = 'lists/list_confirm_delete.html'
    success_url = reverse_lazy('list_list')

    def form_valid(self, form):
        AuditEvent.log(
            actor=self.request.user,
            entity_type='ShoppingList',
            entity_id=self.object.id,
            action='delete',
        )
        messages.success(self.request, 'Lista eliminada.')
        return super().form_valid(form)


class ShareListView(EditorRequiredMixin, FormView):
    """Share a list with another user by email."""
    form_class = ShareListForm
    template_name = 'lists/list_detail.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.shopping_list = get_object_or_404(ShoppingList, pk=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        email = form.cleaned_data['email']
        role = form.cleaned_data['role']

        try:
            user = User.objects.get(email=email)
            # Check if already a member
            if ListMember.objects.filter(list=self.shopping_list, user=user).exists():
                messages.warning(self.request, f'{email} ya es miembro de esta lista.')
                return redirect('list_detail', pk=self.shopping_list.pk)
            # Add directly
            ListMember.objects.create(
                list=self.shopping_list,
                user=user,
                role=role,
                invited_by=self.request.user,
                accepted_at=timezone.now(),
            )
            AuditEvent.log(
                actor=self.request.user,
                entity_type='ListMember',
                entity_id=f'{self.shopping_list.id}:{user.id}',
                action='share',
            )
            messages.success(self.request, f'{email} agregado como {role}.')
        except User.DoesNotExist:
            # Send invitation by email (simplified: create invitation)
            token = uuid.uuid4().hex
            Invitation.objects.create(
                list=self.shopping_list,
                email=email,
                token=token,
                role=role,
                invited_by=self.request.user,
                expires_at=timezone.now() + timedelta(days=7),
            )
            AuditEvent.log(
                actor=self.request.user,
                entity_type='Invitation',
                entity_id=token,
                action='invite',
            )
            messages.info(
                self.request,
                f'Invitación enviada a {email}. Deberán registrarse para aceptarla.',
            )

        return redirect('list_detail', pk=self.shopping_list.pk)

    def form_invalid(self, form):
        return redirect('list_detail', pk=self.shopping_list.pk)


class ShareByTokenView(EditorRequiredMixin, View):
    """Generate or regenerate a share link for the list."""

    def post(self, request, *args, **kwargs):
        shopping_list = get_object_or_404(ShoppingList, pk=kwargs['pk'])
        shopping_list.share_token = uuid.uuid4()
        shopping_list.share_token_expires_at = timezone.now() + timedelta(days=30)
        shopping_list.save(update_fields=['share_token', 'share_token_expires_at'])
        messages.success(request, 'Enlace de compartición generado.')
        return redirect('list_detail', pk=shopping_list.pk)


class AcceptInvitationView(LoginRequiredMixin, View):
    """Accept an invitation by token."""

    def get(self, request, token):
        invitation = get_object_or_404(Invitation, token=token, status='pending')

        if invitation.expires_at < timezone.now():
            invitation.status = 'expired'
            invitation.save(update_fields=['status'])
            messages.error(request, 'Esta invitación ha expirado.')
            return redirect('list_list')

        # Check if already a member
        if ListMember.objects.filter(list=invitation.list, user=request.user).exists():
            messages.warning(request, 'Ya eres miembro de esta lista.')
            return redirect('list_detail', pk=invitation.list.pk)

        ListMember.objects.create(
            list=invitation.list,
            user=request.user,
            role=invitation.role,
            invited_by=invitation.invited_by,
            accepted_at=timezone.now(),
        )
        invitation.status = 'accepted'
        invitation.save(update_fields=['status'])

        AuditEvent.log(
            actor=request.user,
            entity_type='ListMember',
            entity_id=f'{invitation.list.id}:{request.user.id}',
            action='share',
        )
        messages.success(request, f'¡Te has unido a la lista "{invitation.list.name}"!')
        return redirect('list_detail', pk=invitation.list.pk)


class RevokeMemberView(OwnerRequiredMixin, View):
    """Remove a member from the list."""

    def post(self, request, *args, **kwargs):
        shopping_list = get_object_or_404(ShoppingList, pk=kwargs['pk'])
        member_id = kwargs.get('member_id')
        member = get_object_or_404(ListMember, pk=member_id, list=shopping_list)

        if member.role == ListMember.RoleChoices.OWNER:
            messages.error(request, 'No puedes eliminar al propietario.')
            return redirect('list_detail', pk=shopping_list.pk)

        AuditEvent.log(
            actor=request.user,
            entity_type='ListMember',
            entity_id=f'{shopping_list.id}:{member.user.id}',
            action='revoke',
        )
        member.delete()
        messages.success(request, f'{member.user} ha sido eliminado de la lista.')
        return redirect('list_detail', pk=shopping_list.pk)
