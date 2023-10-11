from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
# Create your models here.


class Image(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/', max_length=100, 
                              validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class ExpiringLink(models.Model):
    base_image = models.ForeignKey(Image, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='expiring/%Y/%m/%d/', max_length=100)
    seconds = models.PositiveIntegerField(default=30, validators=[MaxValueValidator(30000), 
                                                                  MinValueValidator(30)])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class ThumbnailSize(models.Model):
    size_name = models.CharField(max_length=50, unique=True)
    size = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Thumbnail size: {self.size} px"


class Thumbnail(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    base_image = models.ForeignKey(Image, related_name='thumbnails', on_delete=models.CASCADE)
    thumbnail_image = models.ImageField(upload_to='thumbnails/%Y/%m/%d/', max_length=100)
    thumbnail_size = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.thumbnail_image)


class AccountTier(models.Model):
    tier_number = models.AutoField(primary_key=True, unique=True, editable=True)
    tier_name = models.CharField(max_length=50, unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.tier_number}. {self.tier_name}"


class GrantedTier(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_tier = models.ForeignKey(AccountTier, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} has {self.account_tier.tier_name} privileges"


# section of classes for granting privileges to account tiers
class ThumbnailGrantedPrivileges(models.Model):
    account_tier = models.ForeignKey(AccountTier, on_delete=models.CASCADE)
    thumbnail_size = models.ForeignKey(ThumbnailSize, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.account_tier.tier_name} tier has '{self.thumbnail_size.size} px thumbnail' option"


class LinkToOriginalGrantedPrivileges(models.Model):
    account_tier = models.ForeignKey(AccountTier, on_delete=models.CASCADE)
    link_to_original_image = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account_tier.tier_name} tier {'has' if self.link_to_original_image==True else 'has not'} 'link to original image' option"


class ExpiringLinkGrantedPrivileges(models.Model):
    account_tier = models.ForeignKey(AccountTier, on_delete=models.CASCADE)
    expiring_link = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.account_tier.tier_name} tier {'has' if self.expiring_link==True else 'has not'} 'create expiring links' option"


    




