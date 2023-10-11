from rest_framework import permissions
from .models import GrantedTier, ExpiringLinkGrantedPrivileges

    
class CreateExpiringLinkPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        granted_tiers = GrantedTier.objects.filter(user=user)
        can_create_expiring_links = ExpiringLinkGrantedPrivileges.objects.filter(
            account_tier__in=[tier.account_tier for tier in granted_tiers], expiring_link=True)
        if can_create_expiring_links:
            return True
        return False
