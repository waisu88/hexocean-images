from django.core.files.base import ContentFile

from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.viewsets import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .models import Image, Thumbnail, GrantedTier, ThumbnailGrantedPrivileges, ExpiringLink, LinkToOriginalGrantedPrivileges
from .serializers import ImageSerializer, ImageLinkToOriginalSerializer, ThumbnailSerializer, ExpiringLinkSerializer
from .permissions import CreateExpiringLinkPermission
from .tasks import delete_expiring_link

from easy_thumbnails.files import get_thumbnailer



class ImagesApiOverview(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        routes = {
            "For LOGIN visit -->": request.build_absolute_uri(reverse(('authorization'))),
            "List-Create images": request.build_absolute_uri(reverse(('list-create-image'))),
            "Thumbnail list": request.build_absolute_uri(reverse(('thumbnail-list'))),
            "Below": "<int:pk> --> image id",
            "Image detail": request.build_absolute_uri(reverse(('list-create-image'))) + "<int:pk>/",
            "Expiring link": request.build_absolute_uri(reverse(('list-create-image'))) + "<int:pk>/expiring-link/",
        }
        return Response(routes)

class ImageListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer

    # returns image serializer depending on permission to preview original image
    def get_serializer_class(self): 
        granted_tiers = GrantedTier.objects.filter(user=self.request.user)
        can_get_original_img = LinkToOriginalGrantedPrivileges.objects.filter(
            account_tier__in=[tier.account_tier for tier in granted_tiers], link_to_original_image=True)
        if can_get_original_img:
            return ImageLinkToOriginalSerializer
        return super().get_serializer_class()

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user is not None:
            return Image.objects.select_related('uploaded_by').filter(uploaded_by=user.id)

    def perform_create(self, image_serializer):
        user = self.request.user
        image_serializer.save(uploaded_by=user)
        self.create_thumbnails(user) 

    def create_thumbnails(self, user):
        print(user)
        base_image = Image.objects.filter(uploaded_by=user).last()
        print(base_image)
        granted_tiers = GrantedTier.objects.filter(user=user)
        account_tiers = [tier.account_tier for tier in granted_tiers]
        print(account_tiers)
        thumbnail_sizes = ThumbnailGrantedPrivileges.objects.filter(account_tier__in=account_tiers)
        available_thumbnail_sizes = []
        print(available_thumbnail_sizes)
        for granted_size in thumbnail_sizes:
            available_thumbnail_sizes.append(granted_size.thumbnail_size.size)
        for th_size in available_thumbnail_sizes:
            thumbnailer = get_thumbnailer(base_image.image)
            th = thumbnailer.get_thumbnail({'size':(th_size, th_size), 'crop': True})
            Thumbnail.objects.create(created_by=user, base_image=base_image, thumbnail_image=str(th), thumbnail_size=th_size)
        

class ImageDetailDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        image_id = self.kwargs['pk']
        user = self.request.user
        return Image.objects.filter(uploaded_by=user, id=image_id)
        
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)



class ThumbnailListApiView(generics.ListAPIView):
    serializer_class = ThumbnailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user is not None:
            return Thumbnail.objects.filter(created_by=user.id)


class ExpiringLinkListCreateAPIView(generics.ListCreateAPIView):
    
    # custom permission class allows entering only users with ability to fetch expiring links
    permission_classes = [IsAuthenticated, CreateExpiringLinkPermission]
    serializer_class = ExpiringLinkSerializer
    queryset = ExpiringLink.objects.all()
    
    def get_queryset(self, *args, **kwargs):
        image_id = self.kwargs['pk']
        user = self.request.user
        if user is not None:
            return ExpiringLink.objects.filter(created_by=user.id, base_image__id=image_id)

    def perform_create(self, expiring_link_serializer):
        user = self.request.user
        image_id = self.kwargs['pk']
        base_image = Image.objects.get(uploaded_by=user, id=image_id)

        # creating copy of image as expiring link instance
        picture_copy = ContentFile(base_image.image.read())
        new_picture_name = base_image.image.name.split("/")[-1]
        expiring_link_serializer.save(created_by=user, base_image=base_image)
        instance = ExpiringLink.objects.filter(created_by=user).last()
        instance.image.save(new_picture_name, picture_copy)
        params = {"instance_id": instance.id,
                  "seconds": instance.seconds}
        # celery task to delete object after given time (seconds)
        delete_expiring_link.delay(params)
        


            
        