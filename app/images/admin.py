from django.contrib import admin
from .models import (
AccountTier, 
GrantedTier, 
Image, 
ExpiringLink,
Thumbnail,
ThumbnailSize, 
ExpiringLinkGrantedPrivileges, 
LinkToOriginalGrantedPrivileges, 
ThumbnailGrantedPrivileges)

# Register your models here.
admin.site.register(
    (AccountTier, GrantedTier, Image, Thumbnail, ExpiringLink,
     ThumbnailSize, ExpiringLinkGrantedPrivileges, 
     LinkToOriginalGrantedPrivileges, ThumbnailGrantedPrivileges))