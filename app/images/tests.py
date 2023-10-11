from .models import Image, Thumbnail, AccountTier, GrantedTier, ExpiringLink, ExpiringLinkGrantedPrivileges, LinkToOriginalGrantedPrivileges
from .permissions import CreateExpiringLinkPermission
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import datetime
from django.core.exceptions import ValidationError


class ImagesAPIViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="davinci", password="very-strong-password")
        self.client.login(username='davinci', password='very-strong-password')
        self.permission = CreateExpiringLinkPermission()
        AccountTier.objects.create(tier_number=1, tier_name="Enterprise")
        GrantedTier.objects.create(user=self.user, account_tier=AccountTier.objects.get(tier_name="Enterprise"))
        ExpiringLinkGrantedPrivileges.objects.create(account_tier=AccountTier.objects.get(tier_name="Enterprise"), expiring_link=True)
        LinkToOriginalGrantedPrivileges.objects.create(account_tier=AccountTier.objects.get(tier_name="Enterprise"), link_to_original_image=True)
        # set-up for testing detail-image
        Image.objects.create(id=1, image="image.png", uploaded_by=self.user, created_at=datetime.datetime.now())
        Image.objects.create(id=2, image="image.jpg", uploaded_by=self.user, created_at=datetime.datetime.now())
        Thumbnail.objects.create(id=1, created_by=self.user, base_image=Image.objects.get(id=1), 
                                 thumbnail_image="th_img.png", thumbnail_size=200, 
                                 created_at=datetime.datetime.now())
        
    def test_images_list_authenticated(self):
        response = self.client.get(reverse("list-create-image"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_images_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("list-create-image"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_image_detail_authenticated(self):
        response = self.client.get(reverse("image-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_image_detail_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("image-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_expiring_link_authenticated(self):
        response = self.client.get(reverse("expiring-links", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_expiring_link_no_permission(self):
        exp_link_obj = ExpiringLinkGrantedPrivileges.objects.get(account_tier__tier_name="Enterprise")
        exp_link_obj.expiring_link = False
        exp_link_obj.save()
        response = self.client.get(reverse("expiring-links", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_expiring_link_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("expiring-links", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_image(self):
        object = Image.objects.get(id=1)
        self.assertIsInstance(object, Image)

    def test_create_image_bad_extension_bmp(self):
        Image.objects.create(id=4, image="img.bmp", uploaded_by=self.user, created_at=datetime.datetime.now())
        object = Image.objects.get(id=4)
        self.assertRaises(ValidationError, object.full_clean)
    
    def test_create_image_bad_extension_pdf(self):
        Image.objects.create(id=5, image="img.pdf", uploaded_by=self.user, created_at=datetime.datetime.now())
        object = Image.objects.get(id=5)
        self.assertRaises(ValidationError, object.full_clean)

    def test_create_image_bad_extension_tiff(self):
        Image.objects.create(id=6, image="img.tiff", uploaded_by=self.user, created_at=datetime.datetime.now())
        object = Image.objects.get(id=6)
        self.assertRaises(ValidationError, object.full_clean)

    def test_create_image_bad_extension_svg(self):
        Image.objects.create(id=7, image="img.svg", uploaded_by=self.user, created_at=datetime.datetime.now())
        object = Image.objects.get(id=7)
        self.assertRaises(ValidationError, object.full_clean)

    def test_create_thumbnail(self):
        object = Thumbnail.objects.get(id=1)
        self.assertIsInstance(object, Thumbnail)

    def test_create_expiring_link(self):
        ExpiringLink.objects.create(base_image=Image.objects.get(id=1), image="exp_im.png", 
                                    seconds=30, created_by=self.user)
        object = ExpiringLink.objects.last()
        self.assertIsInstance(object, ExpiringLink)

    def test_create_expiring_link_less_seconds(self):
        ExpiringLink.objects.create(base_image=Image.objects.get(id=1), image="exp_im.png", 
                                    seconds=20, created_by=self.user)
        object = ExpiringLink.objects.last()
        self.assertRaises(ValidationError, object.full_clean)

    def test_create_expiring_link_more_seconds(self):
        ExpiringLink.objects.create(base_image=Image.objects.get(id=1), image="exp_im.png", 
                                    seconds=30001, created_by=self.user)
        object = ExpiringLink.objects.last()
        self.assertRaises(ValidationError, object.full_clean)
    