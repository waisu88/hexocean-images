from rest_framework import serializers
from .models import Image, Thumbnail, ExpiringLink



class ThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thumbnail
        read_only_fields = ['thumbnail_image', 'base_image']
        fields = "__all__"


# basic image serializer covering full path to image for unprivileged users
class ImageSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, required=False)

    class Meta:
        model = Image
        fields = ['id', 'image', 'uploaded_by', 'created_at', 'thumbnails'] 
        read_only_fields = ['uploaded_by', 'thumbnails']  
        
    def to_representation(self, instance):
        representation = super(ImageSerializer, self).to_representation(instance)
        representation['image'] = instance.image.name.split("/")[-1]
        return representation


# image serializer for better tier owners
class ImageLinkToOriginalSerializer(serializers.ModelSerializer):
    thumbnails = ThumbnailSerializer(many=True, required=False)

    class Meta:
        model = Image
        fields = ['id', 'image', 'uploaded_by', 'created_at', 'thumbnails']    
        read_only_fields = ['uploaded_by', 'thumbnails']  


class ExpiringLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = "__all__"    
        read_only_fields = ['image', 'created_by', 'base_image']


