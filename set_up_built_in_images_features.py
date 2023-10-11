from django.contrib.auth.models import User
from app.images.models import (AccountTier, GrantedTier, ThumbnailSize, 
                           ThumbnailGrantedPrivileges, ExpiringLinkGrantedPrivileges, 
                           LinkToOriginalGrantedPrivileges)


def set_up_built_in_images_features():
    User.objects.create(username="Testuser1", password="Super-strong-pass")
    User.objects.create(username="Testuser2", password="Super-strong-pass")
    User.objects.create(username="Testuser3", password="Super-strong-pass")

    AccountTier.objects.create(tier_number=1, tier_name="Basic")
    AccountTier.objects.create(tier_number=2, tier_name="Premium")
    AccountTier.objects.create(tier_number=1, tier_name="Enterprise")

    ThumbnailSize.objects.create(size_name="200", size=200)
    ThumbnailSize.objects.create(size_name="400", size=400)

    GrantedTier.objects.create(user__username="Testuser1", account_tier__tier_name="Basic")
    GrantedTier.objects.create(user__username="Testuser2", account_tier__tier_name="Premium")
    GrantedTier.objects.create(user__username="Testuser3", account_tier__tier_name="Enterprise")

    ThumbnailGrantedPrivileges.objects.create(account_tier__tier_name="Basic", thumbnail_size__size=200)
    ThumbnailGrantedPrivileges.objects.create(account_tier__tier_name="Premium", thumbnail_size__size=200)
    ThumbnailGrantedPrivileges.objects.create(account_tier__tier_name="Enterprise", thumbnail_size__size=200)
    ThumbnailGrantedPrivileges.objects.create(account_tier__tier_name="Premium", thumbnail_size__size=400)
    ThumbnailGrantedPrivileges.objects.create(account_tier__tier_name="Enterprise", thumbnail_size__size=400)

    ExpiringLinkGrantedPrivileges.objects.create(account_tier__tier_name="Enterprise", expiring_link=True)

    LinkToOriginalGrantedPrivileges.objects.create(account_tier__tier_name="Premium", link_to_original_image=True)
    LinkToOriginalGrantedPrivileges.objects.create(account_tier__tier_name="Enterprise", link_to_original_image=True)


set_up_built_in_images_features()
