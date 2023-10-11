from django.contrib.auth.models import User
from images.models import (AccountTier, GrantedTier, ThumbnailSize, 
                           ThumbnailGrantedPrivileges, ExpiringLinkGrantedPrivileges, 
                           LinkToOriginalGrantedPrivileges)
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        User.objects.create_user("Testuser1", None, "Super-strong-pass")
        User.objects.create_user("Testuser2", None, "Super-strong-pass")
        User.objects.create_user("Testuser3", None, "Super-strong-pass")

        AccountTier.objects.create(tier_number=1, tier_name="Basic")
        AccountTier.objects.create(tier_number=2, tier_name="Premium")
        AccountTier.objects.create(tier_number=3, tier_name="Enterprise")

        ThumbnailSize.objects.create(size_name="200", size=200)
        ThumbnailSize.objects.create(size_name="400", size=400)

        GrantedTier.objects.create(user=User.objects.get(username="Testuser1"), account_tier=AccountTier.objects.get(tier_name="Basic"))
        GrantedTier.objects.create(user=User.objects.get(username="Testuser2"), account_tier=AccountTier.objects.get(tier_name="Premium"))
        GrantedTier.objects.create(user=User.objects.get(username="Testuser3"), account_tier=AccountTier.objects.get(tier_name="Enterprise"))

        ThumbnailGrantedPrivileges.objects.create(account_tier=AccountTier.objects.get(tier_name="Basic"), thumbnail_size=ThumbnailSize.objects.get(size=200))
        ThumbnailGrantedPrivileges.objects.create(account_tier=AccountTier.objects.get(tier_name="Premium"), thumbnail_size=ThumbnailSize.objects.get(size=200))
        ThumbnailGrantedPrivileges.objects.create(account_tier=AccountTier.objects.get(tier_name="Enterprise"), thumbnail_size=ThumbnailSize.objects.get(size=200))
        ThumbnailGrantedPrivileges.objects.create(account_tier=AccountTier.objects.get(tier_name="Premium"), thumbnail_size=ThumbnailSize.objects.get(size=400))
        ThumbnailGrantedPrivileges.objects.create(account_tier=AccountTier.objects.get(tier_name="Enterprise"), thumbnail_size=ThumbnailSize.objects.get(size=400))

        ExpiringLinkGrantedPrivileges.objects.create(account_tier=AccountTier.objects.get(tier_name="Enterprise"), expiring_link=True)

        LinkToOriginalGrantedPrivileges.objects.create(account_tier=AccountTier.objects.get(tier_name="Premium"), link_to_original_image=True)
        LinkToOriginalGrantedPrivileges.objects.create(account_tier=AccountTier.objects.get(tier_name="Enterprise"), link_to_original_image=True)



